def make_background_surface(self):
    self.background_surface.fill(GRAY)

    if self.grid_enabled:
        self.grid.draw(self.background_surface, WINDOW_WIDTH, WINDOW_HEIGHT)

    #Draw objects
    for obj in self.objects:
        if(obj.obj_type != "Neuron" or (obj.obj_type == "Neuron" and obj.inv)):
            obj.draw(self.background_surface)
        if obj.collision_box:
            #obj.collision_box.draw(self.background_surface)
            pass

    #Draw buttons
    for b in self.buttons:
        b.draw(self.background_surface)
        if b.collision_box:
            #b.collision_box.draw(self.background_surface)
            pass

    #Draw labels
    for l in self.labels:
        l.draw(self.background_surface)
        if l.collision_box:
            #l.collision_box.draw(self.background_surface)
            pass
