extends Label

const colors = [Color(1.0, 0.0, 0.0), Color(1.0, 1.0, 0.0), Color(0.0, 1.0, 0.0)]
var current_color_index : int = 2
var fps : int = 0

func _ready():
	pass
	
func _process(_delta):
	fps = int(Engine.get_frames_per_second())
	
	if(fps < 30):
		current_color_index = 0
	elif(fps < 60):
		current_color_index = 1
	else:
		current_color_index = 2
	
	self.set_text(str(fps))
	self.add_color_override("font_color", colors[current_color_index])
	
	
