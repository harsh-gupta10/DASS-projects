import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crow and Vulture Game")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0,0,255)
GREEN = (0,255,0)
CYAN = (51,243,255)
PINK = (249,51,255)
NoOfCrows = 7

star_vertices = [
        (400, 100), (500, 300), (700, 300), (550, 400), (600, 600),
        (400, 500), (200, 600), (250, 400), (100, 300), (300, 300)
    ]


MovablePaths=[
    (10,2),
    (1,3,4,10),
    (2,4),
    (2,3,5,6),
    (4,6),
    (4,5,7,8),
    (6,8),
    (6,9,10,7),
    (8,10),
    (8,9,1,2),
]

BlockMove=[
    [(2,4),(10,8)],
    [(10,9),(4,5)],
    [(2,10),(4,6)],
    [(2,1),(6,7)],
    [(4,2),(6,8)],
    [(8,9),(4,3)],
    [(6,4),(8,10)],
    [(6,5),(10,1)],
    [(8,6),(10,2)],
    [(2,3),(8,7)],
]
occupied = [0,0,0,0,0,0,0,0,0,0]
DeadCrow = 0
NoOfPlacedCrow=0

def FindNearstIndx(pos):
    for i in range(len(star_vertices)):
            distance = ((pos[0] - star_vertices[i][0])**2 + (pos[1] - star_vertices[i][1])**2) ** 0.5
            if distance <= 10:
                return i;

def FindCrowIndexInCrows(StarIndex):
    pos = star_vertices[StarIndex]
    for i in range(len(crow_player.crows)):
            distance = ((pos[0] - crow_player.crows[i][0])**2 + (pos[1] - crow_player.crows[i][1])**2) ** 0.5
            if distance <= 10:
                return i;


def IsIndexInNeighBourCrow(NewPos):
    NewIndex = FindNearstIndx(NewPos)
    print(NewIndex)
    pos = crow_player.crows[crow_player.selected_crow_index]
        # print("Pos", pos)
    ind = FindNearstIndx(pos)
    if ind is not None:
        Neighbors = MovablePaths[ind]
        for item in Neighbors:
            if item -1== NewIndex:
                return True
        return False

def IsIndexInNeighBourVulture(NewPos):
    global DeadCrow
    NewIndex = FindNearstIndx(NewPos)
    print(NewIndex)
    pos = vulture_player.vulture_position
    ind = FindNearstIndx(pos)
    if ind is not None:
        Neighbors = MovablePaths[ind]
        for item in Neighbors:
            if item -1== NewIndex:
                return True
        PossibleSkip = BlockMove[ind]
        for item in PossibleSkip:
            if occupied[item[0]-1]==1:
                if item[1] -1== NewIndex:
                    # ! CROW KO MARO BHI
                    crowIndex = FindCrowIndexInCrows(item[0]-1)
                    DeadCrow+=1
                    occupied[item[0]-1]=0
                    crow_player.crows.pop(crowIndex)
                    return True
        return False


def ValtureBlockedByCrow():
    if vulture_player.vulture_position is None:
        return False
    VultureIndex = FindNearstIndx(vulture_player.vulture_position)
    # NoOfOccupied = 0
    isEveryOccupied = True
    for item in MovablePaths[VultureIndex]:
        if occupied[item-1]==0:
            isEveryOccupied = False
    for item in BlockMove[VultureIndex]:
        if occupied[item[0]-1]==0 or occupied[item[1]-1]==0:
            isEveryOccupied = False
    return isEveryOccupied


# Function to draw the star pattern
def draw_star_pattern():
    font = pygame.font.Font(None, 36)
    for i in range(len(star_vertices)):
        pygame.draw.line(screen, WHITE, star_vertices[i], star_vertices[(i + 1) % len(star_vertices)], 4)
    pygame.draw.line(screen, WHITE, star_vertices[1], star_vertices[(3) % len(star_vertices)], 4)
    pygame.draw.line(screen, WHITE, star_vertices[3], star_vertices[(5) % len(star_vertices)], 4)
    pygame.draw.line(screen, WHITE, star_vertices[5], star_vertices[(7) % len(star_vertices)], 4)
    pygame.draw.line(screen, WHITE, star_vertices[7], star_vertices[(9) % len(star_vertices)], 4)
    pygame.draw.line(screen, WHITE, star_vertices[9], star_vertices[(1) % len(star_vertices)], 4)
    

    for i in range(10):
        pygame.draw.circle(screen, WHITE, star_vertices[i], 14)  # Placeholder for vulture
        # turn_surface = font.render(str(i), True, GREEN)  # Convert i to a string
        # screen.blit(turn_surface, star_vertices[i]+(10,10))

def HilightCircleCrow():
    if crow_player.selected_crow_index is not None:
        pos = crow_player.crows[crow_player.selected_crow_index]
        ind = FindNearstIndx(pos)
        if ind is not None:
            Neighbors = MovablePaths[ind]
            for item in Neighbors:
                if occupied[item-1]==0:
                    pygame.draw.circle(screen, CYAN, star_vertices[item-1], 18, 4) 

def HilightCircleVulture():
    if vulture_player.vulture_position is not None and current_player==vulture_player:
        pos = vulture_player.vulture_position
        ind = FindNearstIndx(pos)
        if ind is not None:
            Neighbors = MovablePaths[ind]
            for item in Neighbors:
                if occupied[item-1]==0:
                    pygame.draw.circle(screen, PINK, star_vertices[item-1], 18, 4) 
            PossibleSkip = BlockMove[ind]
            for item in PossibleSkip:
                if occupied[item[0]-1]==1:
                    if occupied[item[1]-1]==0:
                        pygame.draw.circle(screen, PINK, star_vertices[item[1]-1], 18, 4)

class CrowPlayer:
    def __init__(self):
        self.crows = []
        self.selected_crow_index = None
    def CheckIfInPlaceholder(position):
            for vertex in star_vertices:
                distance = ((position[0] - vertex[0])**2 + (position[1] - vertex[1])**2) ** 0.5
                if distance < 8:
                    return True
            return False

    def place_crow(self,position):
        if CrowPlayer.CheckIfInPlaceholder(position) and occupied[FindNearstIndx(position)]==0: 
            self.crows.append(position)
            occupied[FindNearstIndx(position)]=1
            return True
        else:
            print('Shi jagah chalo Crow Inital')
            return False


    def select_crow(self, position):
        for i, crow_position in enumerate(self.crows):
            distance = ((position[0] - crow_position[0])**2 + (position[1] - crow_position[1])**2) ** 0.5
            if distance <= 10:  
                self.selected_crow_index = i
                
                return True
        return False

    def move_selected_crow(self, new_position):
        if self.selected_crow_index is not None:
            if CrowPlayer.CheckIfInPlaceholder(new_position) and occupied[FindNearstIndx(new_position)]==0 and IsIndexInNeighBourCrow(new_position)==True:
                occupied[FindNearstIndx(self.crows[self.selected_crow_index])]=0
                self.crows[self.selected_crow_index] = new_position
                occupied[FindNearstIndx(new_position)]=1
                self.selected_crow_index = None
                return True
            else:
                print('Shi jagah chalo Crow Later')
                return False



class VulturePlayer:
    def __init__(self):
        self.vulture_position = None

    def CheckIfInPlaceholder(position):
            for vertex in star_vertices:
                distance = ((position[0] - vertex[0])**2 + (position[1] - vertex[1])**2) ** 0.5
                if distance < 8:
                    return True
            return False

    def place_vulture(self, position):
        if CrowPlayer.CheckIfInPlaceholder(position) and occupied[FindNearstIndx(position)]==0:
            self.vulture_position = position
            occupied[FindNearstIndx(self.vulture_position)]=1
            return True
        else:
            print('Shi jagah chalo Vulture')
            return False

    def move_vulture(self, new_position):
        if CrowPlayer.CheckIfInPlaceholder(new_position) and occupied[FindNearstIndx(new_position)]==0 and IsIndexInNeighBourVulture(new_position)==True:
            occupied[FindNearstIndx(self.vulture_position)]=0
            self.vulture_position = new_position
            occupied[FindNearstIndx(self.vulture_position)]=1
            return True
        else:
            print('Shi jagah chalo Vulture')
            return False


crow_player = CrowPlayer()
vulture_player = VulturePlayer()

def main():
    global current_player
    current_player = crow_player
    font = pygame.font.Font(None, 36)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif ValtureBlockedByCrow():
                crow_won_text = font.render("Crow won!", True, WHITE)
                screen.blit(crow_won_text, (screen.get_width() // 2 - crow_won_text.get_width() // 2, screen.get_height() // 2 - crow_won_text.get_height() // 2))
                pygame.display.flip()
                pygame.time.delay(2000)  
                running = False
            elif DeadCrow >=4:
                VultureTextWon = font.render("Vulture won!", True, WHITE)
                screen.blit(VultureTextWon, (screen.get_width() // 2 - VultureTextWon.get_width() // 2, screen.get_height() // 2 - VultureTextWon.get_height() // 2))
                pygame.display.flip()
                pygame.time.delay(2000)  
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Handle player input
                if current_player == crow_player:
                    global NoOfPlacedCrow
                    if NoOfPlacedCrow < NoOfCrows:
                        position = pygame.mouse.get_pos()
                        if current_player.place_crow(position)==True:
                            NoOfPlacedCrow+=1
                            current_player = vulture_player
                    else:
                        if current_player.selected_crow_index == None:
                            position = pygame.mouse.get_pos()
                            current_player.select_crow(position)
                        else:
                            position = pygame.mouse.get_pos()
                            Starind = FindNearstIndx(position)
                            if Starind:
                                CrowInd = FindCrowIndexInCrows(Starind)
                                if CrowInd==crow_player.selected_crow_index:
                                    crow_player.selected_crow_index=None
                                elif current_player.move_selected_crow(position)==True:
                                    current_player = vulture_player
                else:
                    position = pygame.mouse.get_pos()
                    if vulture_player.vulture_position==None:
                        if vulture_player.place_vulture(position)==True:
                            current_player = crow_player
                    else:
                        if vulture_player.move_vulture(position)==True:
                            current_player = crow_player
        screen.fill(BLACK)
        draw_star_pattern()
        # Draw crows and vulture
        for crow_position in crow_player.crows:
            pygame.draw.circle(screen, CYAN, crow_position, 18)
        if vulture_player.vulture_position:
            pygame.draw.circle(screen, PINK, vulture_player.vulture_position, 18)
        turn_text = "Player's Turn: Crow" if current_player == crow_player else "Player's Turn: Vulture"
        turn_surface = font.render(turn_text, True, WHITE)
        screen.blit(turn_surface, (10, 10))
        for i in range(NoOfCrows - NoOfPlacedCrow):
            pygame.draw.circle(screen, CYAN, (30, 100 + i * 30), 10)
        for i in range(DeadCrow):
            pygame.draw.circle(screen, CYAN, (670, 100 + i * 30), 10)
        HilightCircleCrow()
        HilightCircleVulture()
        # print(occupied)
        pygame.display.flip()

if __name__ == "__main__":
    main()

