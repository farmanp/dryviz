import sys
import wrapt
from rich.console import Console, Group # Changed import for Group
from rich.text import Text
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, RichLog
from .visuals import render_linked_list, render_tree, render_graph, render_stack, render_dict

console = Console()

# Renderer Registry
RENDERER_REGISTRY = []

def register_renderer(condition_func, render_func):
    """Registers a new renderer strategy."""
    RENDERER_REGISTRY.append((condition_func, render_func))

# --- Condition and Render Functions for Specific Types (Modified to return renderables) ---

def _can_render_linked_list(var_name, _var_value): # Mark _var_value as unused
    return var_name == 'head'

def _render_linked_list_var(var_name, var_value):
    # Returns a Rich Group containing the variable name and its visualization
    return Group(Text(f"  {var_name}:"), render_linked_list(var_value))

def _is_graph_like_dict(var_value):
    if not isinstance(var_value, dict) or not var_value:
        return False
    for _, v_list in var_value.items(): # Mark _ as unused
        if not isinstance(v_list, list):
            return False
    return any(var_value.values())

def _can_render_graph_dict(_var_name, var_value): # Mark _var_name as unused
    return _is_graph_like_dict(var_value)

def _render_graph_dict_var(var_name, var_value):
    # Returns a Rich Group
    return Group(Text(f"  {var_name} (Graph):"), render_graph(var_value, name=var_name))

def _can_render_generic_dict(_var_name, var_value): # Mark _var_name as unused
    return isinstance(var_value, dict)

def _render_generic_dict_var(var_name, var_value):
    # Returns a Rich Group
    return Group(Text(f"  {var_name} (Dictionary):"), render_dict(var_value, name=var_name))

def _can_render_stack(var_name, var_value):
    return isinstance(var_value, list) and var_name.lower() in ['stack', 's', 'stk']

def _render_stack_var(var_name, var_value):
    # Returns a Rich Group
    return Group(Text(f"  {var_name} (Stack):"), render_stack(var_value, name=var_name))

def _can_render_tree_node(var_name, var_value):
    if var_name == 'head' and hasattr(var_value, 'next'):
        return False
    return hasattr(var_value, 'value') and \
           (hasattr(var_value, 'children') or \
            hasattr(var_value, 'left') or \
            hasattr(var_value, 'right'))

def _render_tree_node_var(var_name, var_value):
    # Returns a Rich Group
    return Group(Text(f"  {var_name} (Tree):"), render_tree(var_value, name=var_name))

# Register renderers (order matters)
register_renderer(_can_render_linked_list, _render_linked_list_var)
register_renderer(_can_render_graph_dict, _render_graph_dict_var)
register_renderer(_can_render_generic_dict, _render_generic_dict_var)
register_renderer(_can_render_stack, _render_stack_var)
register_renderer(_can_render_tree_node, _render_tree_node_var)


def _render_variable(var_name, var_value):
    """Helper function to get a renderable for a single variable using the registry."""
    for can_render, render_func in RENDERER_REGISTRY:
        if can_render(var_name, var_value):
            return render_func(var_name, var_value) # Return the Rich object

    # Default representation for other variables
    try:
        return Text(f"  {var_name}: {var_value}")
    except (TypeError, ValueError, AttributeError) as e:
        return Text(f"  {var_name}: <Object of type {type(var_value).__name__}> (Error rendering: {e})")


class DryvizTraceApp(App):
    """A Textual application to display dry-run traces."""

    BINDINGS = [("q", "quit", "Quit")]
    CSS_PATH = None # No separate CSS file for now

    def __init__(self, trace_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trace_data = trace_data
        self.title = "Dryviz Execution Trace"

    def compose(self) -> ComposeResult:
        yield Header()
        yield RichLog(highlight=True, markup=True, wrap=False, id="trace_log")
        yield Footer()

    async def on_mount(self) -> None:
        """Called when app is mounted."""
        trace_log = self.query_one(RichLog)
        trace_log.write(Text(" ")) # Prime RichLog with a blank line text object
        for step_items_list in self.trace_data: # step_items_list is now a list of renderables
            for renderable_item in step_items_list:
                trace_log.write(renderable_item)
            trace_log.write("---") # Separator between steps


@wrapt.decorator
def dryviz(wrapped, _instance, args, kwargs): # Mark _instance as unused
    """
    Trace function execution, collect data, and display in a Textual app.
    """
    trace_data = [] # Stores lists of Rich renderables for each step

    def tracer(frame, event, _arg): # Mark _arg as unused
        if event == "line" and frame.f_code.co_filename == wrapped.__code__.co_filename:
            lineno = frame.f_lineno
            local_vars = frame.f_locals.copy()
            
            line_header = Text.from_markup(f"[bold cyan]Line {lineno}[/]:") # Changed to Text.from_markup()
            step_renderables = [line_header]

            for var_name, var_value in local_vars.items():
                renderable = _render_variable(var_name, var_value)
                if renderable: # Ensure renderable is not None
                    step_renderables.append(renderable)
            
            trace_data.append(step_renderables) # Changed from Group(*step_renderables)
        return tracer

    sys.settrace(tracer)
    try:
        result = wrapped(*args, **kwargs)
    finally:
        sys.settrace(None)

    # After function execution, launch the Textual app
    if trace_data:
        app = DryvizTraceApp(trace_data=trace_data)
        app.run() # This will block until the app is quit
        
    return result