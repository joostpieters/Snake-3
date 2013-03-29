#!/usr/bin/python
# -*- coding: utf-8 -*- 

# snake.py
# Darío Lumbreras
# Marzo 27, 2013

import cairo
import gobject
import gtk
import random

class Snake:

  def __init__(self, delta, rows, cols):
    self.delta = delta
    self.rows  = rows
    self.cols  = cols

    self.width  = self.delta * self.rows
    self.height = self.delta * self.cols

    self.window = gtk.Window()
    self.window.connect('destroy', gtk.main_quit)
    self.window.set_title('Snake')
    self.window.set_position(gtk.WIN_POS_CENTER)
    self.window.set_resizable(False)

    self.screen = gtk.DrawingArea()
    self.screen.connect('expose-event', self.on_expose_event)
    self.screen.set_size_request(self.width, self.height)

    self.window.add(self.screen)
    self.window.add_events(gtk.gdk.KEY_PRESS_MASK)
    self.window.connect('key-press-event', self.on_key_press_event)
    self.window.show_all()

    self.init()

  def init(self):
    # Dimensiones de la ventana.
    alloc = self.window.allocation

    # Agregamos la cabeza de la serpiente en el medio.
    self.snake = [(alloc.width / 2, alloc.height / 2)]

    # Dirección inicial.
    self.key = gtk.keysyms.Up

    # Establecemos la comida.
    self.food = self.random_position()

    # La serpiente se comió la comida.
    self.success = False

  def random_position(self):
    return self.delta * random.randint(1, self.rows - 1), self.delta * random.randint(1, self.cols - 1)

  def update(self):
    # Actualiza la pantalla.
    window = self.screen.window
    window.invalidate_region(window.get_clip_region(), False)
    window.process_updates(True)

  def on_key_press_event(self, widget, event):
    # Verificar que la tecla sea alguna de las flechas.
    # https://github.com/GNOME/pygtk/blob/master/gtk/keysyms.py
    if event.keyval >= 0xFF51 and event.keyval <= 0xFF54:
      # Evitar cambiar a la dirección opuesta.
      if abs(self.key - event.keyval) != 2:
        self.key = event.keyval

  def on_expose_event(self, widget, event):
    cr = widget.window.cairo_create()

    # Region que se actualizará.
    cr.rectangle(0, 0, self.width, self.height)
    cr.clip()

    # Fondo.
    cr.rectangle(0, 0, self.width, self.height)
    cr.set_source_rgb(0.0, 0.0, 0.0)
    cr.fill_preserve()
    cr.stroke()

    # Coordenadas de la cabeza.
    x, y = self.snake[0]

    # Mover la cabeza de la serpiente.
    if self.key == gtk.keysyms.Left:
      x = x - self.delta
    elif self.key == gtk.keysyms.Up:
      y = y - self.delta
    elif self.key == gtk.keysyms.Right:
      x = x + self.delta
    elif self.key == gtk.keysyms.Down:
      y = y + self.delta

    # Se rebasaron los límites de la pantalla.
    if x < 0 or x >= self.width or y < 0 or y >= self.height:
      pass

    # Tupla con la nueva posición.
    point = x, y

    # La serpiente se tocó asi misma.
    if point in self.snake:
      pass

    # La serpiente se comió la comida.
    if point == self.food:
      self.success = True
      self.snake.append(self.snake[-1])

    # La sensación de movimiento se logra quitando la cola de la serpiente
    # y agregando la cabeza con su nueva posición.
    self.snake.pop()
    self.snake.insert(0, point)

    # Dibujar la serpiente.
    for x, y in self.snake:
      cr.rectangle(x, y, self.delta, self.delta)
      cr.set_source_rgb(0.0, 0.0, 1.0)
      cr.fill_preserve()
      cr.set_source_rgb(0.0, 0.0, 0.0)
      cr.stroke()

    # Volver a colocar la comida si esta fue alcanzada.
    if self.success:
      self.success = False
      self.food = self.random_position()

    # Dibujar la comida.
    cr.rectangle(self.food[0], self.food[1], self.delta, self.delta)
    cr.set_source_rgb(0.0, 1.0, 0.0)
    cr.fill_preserve()
    cr.set_source_rgb(0.0, 0.0, 0.0)
    cr.stroke()

    # Actualiza la pantalla.
    gobject.timeout_add(60, self.update)

  def main(self):
    gtk.main()

def main():
  snake = Snake(10, 30, 30)
  snake.main()

if __name__ == '__main__':
  main()
