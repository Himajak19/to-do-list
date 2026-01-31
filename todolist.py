import ipywidgets as widgets
from IPython.display import display, clear_output

# --- App State ---
# Storing tasks as dictionaries to keep track of their status
tasks = [] 

# --- UI Components ---
title = widgets.HTML("<h1 style='color: #5f6368; font-family: \"Product Sans\", Arial; margin-bottom: 20px;'>My To-do List</h1>")
task_input = widgets.Text(placeholder='Take a note...', layout=widgets.Layout(width='70%'))
add_button = widgets.Button(description='Add', button_style='warning', icon='plus', layout=widgets.Layout(width='15%'))
output_area = widgets.Output()

def render_page():
    with output_area:
        clear_output()
        
        active_box = []
        completed_box = []

        # Logic for Active and Completed tasks
        for index, task_item in enumerate(tasks):
            # Checkbox
            chk = widgets.Checkbox(value=task_item['completed'], description=task_item['text'], indent=False, layout={'width': '85%'})
            
            # Red Dustbin (Icon only, no border)
            del_btn = widgets.Button(icon='trash', layout=widgets.Layout(width='40px', border='none'), style={'button_color': 'transparent'})
            
            # --- Handlers ---
            def toggle_status(change, idx=index):
                tasks[idx]['completed'] = change['new']
                render_page()

            def delete_item(b, idx=index):
                tasks.pop(idx)
                render_page()

            chk.observe(toggle_status, names='value')
            del_btn.on_click(delete_item)

            row = widgets.HBox([chk, del_btn], layout=widgets.Layout(align_items='center', margin='2px 0'))
            
            if task_item['completed']:
                # Applying strikethrough styling to the checkbox label via CSS injection
                completed_box.append(row)
            else:
                active_box.append(row)

        # Display Active Tasks
        if active_box:
            display(widgets.VBox(active_box))
        
        # Display Completed Tasks (with the Keep-style separator)
        if completed_box:
            display(widgets.HTML("<div style='border-top: 1px solid #e0e0e0; margin: 15px 0; padding-top: 10px; color: #5f6368; font-weight: bold;'>+ Completed items</div>"))
            # Make completed items look faded
            display(widgets.VBox(completed_box))

# CSS to handle the red trash icon and strikethrough effect
display(widgets.HTML("""
<style>
    .fa-trash { color: #d93025 !important; opacity: 0.7; }
    .fa-trash:hover { opacity: 1; }
    /* Target labels of checked checkboxes to strike through */
    .widget-checkbox.widget-inline-listbox input:checked + span { 
        text-decoration: line-through; 
        color: #80868b; 
    }
</style>
"""))

def on_add_clicked(b):
    if task_input.value.strip():
        tasks.insert(0, {'text': task_input.value, 'completed': False}) # New tasks at top
        task_input.value = ''
        render_page()

add_button.on_click(on_add_clicked)
task_input.on_submit(on_add_clicked) # Press Enter to add

# --- Final Layout ---
input_section = widgets.HBox([task_input, add_button], layout=widgets.Layout(margin='0 0 20px 0'))
app_container = widgets.VBox([title, input_section, output_area], layout=widgets.Layout(padding='20px', width='100%'))

display(app_container)
render_page()
