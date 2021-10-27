import aStar
import pygame
from threading import *
import time
from graph import Graph

source = "E:/map.bmp"
max_pixel_value = 765
window_size = (250, 250)


def load_image_to(surface):
    surface.blit(pygame.image.load(source), (0, 0))


def calculation_thread(graph, start, target, surface, lock):
    load_image_to(surface)
    font = pygame.font.SysFont("chalkduster.ttf", 24)
    text = font.render("Processing", True, pygame.Color("blue"))
    text_rect = text.get_rect(center=(window_size[0]/2, window_size[1]/2))
    surface.blit(text, text_rect)

    graph.set_heuristics(target)
    path = aStar.calculate(start, target, graph.rev_graph, graph.heuristics)

    speed = window_size[0] + window_size[1]
    load_image_to(surface)
    for node in path:
        surface.set_at(node, (255, 0, 0))
        time.sleep(1 / speed)

    lock.release()


def main():
    lock = Lock()
    graph = Graph(source, max_pixel_value)
    start = (0, 0)

    pygame.init()
    display_surface = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Ścieżka")
    load_image_to(display_surface)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if not lock.locked():
                        lock.acquire()
                        pos = pygame.mouse.get_pos()
                        new_thread = Thread(
                            target=calculation_thread, args=(graph, list(start), list(pos), display_surface, lock,))
                        new_thread.start()
                elif event.button == 3:
                    start = pygame.mouse.get_pos()
                    if not lock.locked():
                        load_image_to(display_surface)
                        display_surface.set_at(list(start), (255, 0, 0))
            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()


if __name__ == '__main__':
    main()
