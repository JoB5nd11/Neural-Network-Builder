extends SpinBox

signal _GridSize_changed

func _ready():
	pass

func _on_Grid_Size_Input_value_changed(value):
	#gets send to Main/GridSizeChanger.gd
	emit_signal('_GridSize_changed', int(value))
