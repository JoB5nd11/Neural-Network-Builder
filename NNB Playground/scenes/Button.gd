extends Button

onready var is_info_shown : bool = false
onready var hover_info = get_parent().get_node("Hover Info")

func _ready():
	pass
	
func _process(delta):
	if(is_info_shown):
		hover_info.set_position(Vector2(get_viewport().get_mouse_position().x + 15, 
										get_viewport().get_mouse_position().y + 15))
	
func _on_Button_mouse_entered():
	hover_info.visible = true
	is_info_shown = true


func _on_Button_mouse_exited():
	hover_info.visible = false
	is_info_shown = false
