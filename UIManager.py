import pygame
import pygame_gui
from nodes import StructureType, TerrainType

class UIManager:
    def __init__(self, window_size):
        self.manager = pygame_gui.UIManager(window_size, "theme.json")
        self.guiPanel = pygame.Rect(0, 0, 220, 500)

        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=self.guiPanel,
            manager=self.manager
        )

        self.boundHeading = pygame_gui.elements.UILabel(
            pygame.Rect(10, 20, 200, 30),
            text="Create Bounds",
            container=self.panel,
            manager=self.manager
        )

        self.brushHeading = pygame_gui.elements.UILabel(
            pygame.Rect(10, 170, 180, 30),
            text="Brush",
            container=self.panel,
            manager=self.manager
        )

        self.structureHeading = pygame_gui.elements.UILabel(
            pygame.Rect(10, 290, 180, 30),
            text="Structures",
            container=self.panel,
            manager=self.manager
        )

        self.removeStructureText = pygame_gui.elements.UILabel(
            pygame.Rect(40, 370, 140, 30),
            text="Remove Structure",
            container=self.panel,
            manager=self.manager
        )

        self.widthInput = pygame_gui.elements.UITextEntryLine(
            pygame.Rect(10, 50, 200, 30),
            placeholder_text="width...",
            container=self.panel,
            manager=self.manager
        )

        self.heightInput = pygame_gui.elements.UITextEntryLine(
            pygame.Rect(10, 90, 200, 30),
            placeholder_text="height...",
            container=self.panel,
            manager=self.manager
        )

        self.applyBoundsButton = pygame_gui.elements.UIButton(
            pygame.Rect(10, 120, 200, 30),
            text="Apply",
            container=self.panel,
            manager=self.manager
        )

        self.terrainButton = pygame_gui.elements.UIButton(
            pygame.Rect(10, 170, 30, 30),
            text='[X]',
            container=self.panel,
            manager=self.manager
        )

        self.brushSizeBar = pygame_gui.elements.UIHorizontalSlider(
            pygame.Rect(10, 200, 160, 30),
            start_value=1,
            value_range=(1, 10),
            container=self.panel,
            manager=self.manager
        )

        self.brushSizeDisplay = pygame_gui.elements.UILabel(
            pygame.Rect(170, 200, 35, 30),
            text='1',
            container=self.panel,
            manager=self.manager
        )

        self.terrainTypeDropdown = pygame_gui.elements.UIDropDownMenu(
            relative_rect=pygame.Rect(10, 240, 180, 30),
            options_list=[t.name for t in TerrainType],
            starting_option=TerrainType.EMPTY.name,
            container=self.panel,
            manager=self.manager
        )

        self.structureButton = pygame_gui.elements.UIButton(
            pygame.Rect(10, 290, 30, 30),
            text='[  ]',
            container=self.panel,
            manager=self.manager
        )

        self.structureTypeDropdown = pygame_gui.elements.UIDropDownMenu(
            relative_rect=pygame.Rect(10, 320, 180, 30),
            options_list=[t.name for t in StructureType],
            starting_option=StructureType.HOUSE.name,
            container=self.panel,
            manager=self.manager
        )

        self.removeStructureButton = pygame_gui.elements.UIButton(
            pygame.Rect(10, 370, 30, 30),
            text='[  ]',
            container=self.panel,
            manager=self.manager
        )

        self.enableGridRendering = pygame_gui.elements.UICheckBox(
            pygame.Rect(10, 420, 30, 30),
            text="Enable Grid Rendering",
            container=self.panel,
            manager=self.manager
        )
        self.enableGridRendering.set_state(True)

        self.submitButton = pygame_gui.elements.UIButton(
            pygame.Rect(10, 460, 200, 30),
            text="Submit",
            container=self.panel,
            manager=self.manager
        )

    def process_event(self, event):
        self.manager.process_events(event)

    def update(self, dt):
        self.manager.update(dt)

    def draw(self, screen):
        self.manager.draw_ui(screen)