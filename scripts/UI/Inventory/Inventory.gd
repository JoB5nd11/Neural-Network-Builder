extends Control


signal _InputNeuron_created
signal _HiddenNeuron_created
signal _OutputNeuron_created

func _ready():
	pass

func _on_Input_Neuron_pressed():
	emit_signal('_InputNeuron_created')

func _on_Hidden_Neuron_pressed():
	emit_signal('_HiddenNeuron_created')

func _on_Output_Neuron_pressed():
	emit_signal('_OutputNeuron_created')
