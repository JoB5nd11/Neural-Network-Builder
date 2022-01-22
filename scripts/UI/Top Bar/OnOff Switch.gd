extends TextureButton

signal _OnOff_toggled

func _ready():
	pass

func _on_OnOff_Switch_toggled(button_pressed):
	emit_signal('_OnOff_toggled', button_pressed)
