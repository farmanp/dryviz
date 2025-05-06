import sys
import wrapt
from rich.console import Console
from .visuals import render_linked_list, render_tree, render_graph, render_stack, render_dict

console = Console()

# Renderer Registry
RENDERER_REGISTRY = []

def register_renderer(condition_func, render_func):
    """Registers a new renderer strategy."""
    RENDERER_REGISTRY.append((condition_func, render_func))

# --- Condition and Render Functions for Specific Types ---

def _can_render_linked_list(var_name, _var_value): # Mark _var_value as unused
    return var_name == 'head'

def _render_linked_list_var(var_name, var_value):
    tree_vis = render_linked_list(var_value)
    console.print(f"  {var_name}:", tree_vis)

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
    tree_vis = render_graph(var_value, name=var_name)
    console.print(f"  {var_name} (Graph):", tree_vis)

def _can_render_generic_dict(_var_name, var_value): # Mark _var_name as unused
    # This should be checked after graph-like dicts
    return isinstance(var_value, dict)

def _render_generic_dict_var(var_name, var_value):
    tree_vis = render_dict(var_value, name=var_name)
    console.print(f"  {var_name} (Dictionary):", tree_vis)

def _can_render_stack(var_name, var_value):
    return isinstance(var_value, list) and var_name.lower() in ['stack', 's', 'stk']

def _render_stack_var(var_name, var_value):
    tree_vis = render_stack(var_value, name=var_name)
    console.print(f"  {var_name} (Stack):", tree_vis)

def _can_render_tree_node(var_name, var_value):
    # Avoid re-rendering linked list nodes if 'head' was already handled
    if var_name == 'head' and hasattr(var_value, 'next'):
        return False
    return hasattr(var_value, 'value') and \
           (hasattr(var_value, 'children') or \
            hasattr(var_value, 'left') or \
            hasattr(var_value, 'right'))

def _render_tree_node_var(var_name, var_value):
    tree_vis = render_tree(var_value, name=var_name)
    console.print(f"  {var_name} (Tree):", tree_vis)

# Register renderers (order matters for overlapping conditions like dicts)
register_renderer(_can_render_linked_list, _render_linked_list_var)
register_renderer(_can_render_graph_dict, _render_graph_dict_var) # Graph dict check before generic dict
register_renderer(_can_render_generic_dict, _render_generic_dict_var)
register_renderer(_can_render_stack, _render_stack_var)
register_renderer(_can_render_tree_node, _render_tree_node_var)


def _render_variable(var_name, var_value):
    """Helper function to render a single variable using the registry."""
    for can_render, render_func in RENDERER_REGISTRY:
        if can_render(var_name, var_value):
            render_func(var_name, var_value)
            return True
    return False

@wrapt.decorator
def dryviz(wrapped, _instance, args, kwargs): # Mark _instance as unused
    """
    Trace function execution line-by-line, visualize data structures,
    and stub side effects during a "dry run."
    """
    def tracer(frame, event, _arg): # Mark _arg as unused
        # Only trace lines within the decorated function's file
        if event == "line" and frame.f_code.co_filename == wrapped.__code__.co_filename:
            lineno = frame.f_lineno
            local_vars = frame.f_locals.copy()
            console.print(f"[bold cyan]Line {lineno}[/]:")

            for var_name, var_value in local_vars.items():
                rendered = _render_variable(var_name, var_value)
                
                if not rendered:
                    # Default print for other variables or if no specific visualizer matched
                    try:
                        # Attempt a more readable representation for simple types
                        console.print(f"  {var_name}: {var_value}")
                    except (TypeError, ValueError, AttributeError) as e: # Catch more specific exceptions
                        console.print(f"  {var_name}: <Object of type {type(var_value).__name__}> (Error rendering: {e})")
            
            input("Press [bold yellow]Enter[/] to continue... ")
        return tracer

    # Begin tracing
    sys.settrace(tracer)
    try:
        result = wrapped(*args, **kwargs)
    finally:
        sys.settrace(None)
    return result