import sys
import wrapt
from rich.console import Console
from .visuals import render_linked_list, render_tree, render_graph, render_stack, render_dict

console = Console()

def _render_variable(var_name, var_value):
    """Helper function to render a single variable."""
    # Attempt to render known structures
    if var_name == 'head':  # Specific convention for linked list head
        tree_vis = render_linked_list(var_value)
        console.print(f"  {var_name}:", tree_vis)
        return True
    elif isinstance(var_value, dict):  # General dictionary
        is_graph_like = True
        if not var_value: # Empty dict is not a graph here
            is_graph_like = False
        else:
            for _, v_list in var_value.items(): # Mark _ as unused
                if not isinstance(v_list, list):
                    is_graph_like = False
                    break
        
        if is_graph_like and any(var_value.values()): # Render as graph
            tree_vis = render_graph(var_value, name=var_name)
            console.print(f"  {var_name} (Graph):", tree_vis)
        else:  # Else, render as a generic dictionary
            tree_vis = render_dict(var_value, name=var_name)
            console.print(f"  {var_name} (Dictionary):", tree_vis)
        return True
    elif isinstance(var_value, list):  # General list, could be a stack
        if var_name.lower() in ['stack', 's', 'stk']:
            tree_vis = render_stack(var_value, name=var_name)
            console.print(f"  {var_name} (Stack):", tree_vis)
            return True
    elif hasattr(var_value, 'value') and \
         (hasattr(var_value, 'children') or \
          hasattr(var_value, 'left') or \
          hasattr(var_value, 'right')):
        # Avoid re-rendering linked list nodes if 'head' was already handled
        if not (var_name == 'head' and hasattr(var_value, 'next')):
            tree_vis = render_tree(var_value, name=var_name)
            console.print(f"  {var_name} (Tree):", tree_vis)
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