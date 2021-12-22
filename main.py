from cmu_graphics import *

# Initialize lists of pieces
whitePieces = []
blackPieces = []
# Pieces will be added when board is drawn
 
# Draw the board and place the pieces
blackRow = False #keeps track of whether the black squares need to be offset

def drawX(row): #draws one row
    if (row):
        x = 0
    else:
        x = 50
    while(x <= 350):
        Rect(x,y,50,50)
        if (y <= 100):
            blackPieces.append(Circle(x+25, y+25, 20, fill='darkslategrey')) #a black piece goes on this square
        if (y >= 250):
            whitePieces.append(Circle(x+25, y+25, 20, fill='white')) #a white piece goes on this square
        x += 100
y = 0

#draws the board by repeatedly calling drawX()
while(y <= 350):
    drawX(blackRow)
    if (blackRow):
        blackRow = False
    else:
        blackRow = True
    y += 50

#initializes the 'king' variable in each piece
for piece in whitePieces:
    piece.king = False
for piece in blackPieces:
    piece.king = False

#Initialize gamestate variables
app.turn = True #True = white's turn, False = black's turn
app.clicks = 0 #tracks how many clicks you've made, to change modes from projecting moves to making moves
    # technically only tracks selections, not total clicks, so you can't pass your turn by mistake
app.canCapture = False
app.selection = None
app.moves = []
app.win = False
            
def getPiece(x, y):
    shape = app.group.hitTest(x, y)
    if (isinstance(shape, Rect) or shape == None):
        return None
    else:
        return shape
        
def captures(piece):
    # Creates a list of lists, containing coordinates of all capturing moves of the given piece
    # List is a list of lists where each sub-list is an ordered pair, i.e. [ [1,2], [102,321] ]
    # Each ordered pair is a pair of coordinates that the piece could move to, if it were to capture an enemy piece.
    captureList = []
    if (app.turn): #it's white's turn
        leftPiece = getPiece(piece.centerX-50, piece.centerY-50)
        rightPiece = getPiece(piece.centerX+50, piece.centerY-50)
        
        if (leftPiece in blackPieces): #if there's a black piece to the left
            if (getPiece(leftPiece.centerX-50, leftPiece.centerY-50) == None): #if there's no piece in the way
                if (leftPiece.centerX-50 > 0 and leftPiece.centerY-50 > 0):
                    captureList.append([piece.centerX-100, piece.centerY-100])
        if (rightPiece in blackPieces): #if there's a black piece to the right
            if (getPiece(rightPiece.centerX+50, rightPiece.centerY-50) == None):
                if (rightPiece.centerX+50 < 400 and rightPiece.centerY-50 > 0):
                    captureList.append([piece.centerX+100, piece.centerY-100])
        if (piece.king):
            bottomLeftPiece = getPiece(piece.centerX-50, piece.centerY+50)
            bottomRightPiece = getPiece(piece.centerX+50, piece.centerY+50)
            if (bottomLeftPiece in blackPieces): #if there's a piece to the left
                if (getPiece(bottomLeftPiece.centerX-50, bottomLeftPiece.centerY+50) == None): #if there's no piece further ahead
                    if (bottomLeftPiece.centerX-50 > 0 and bottomLeftPiece.centerY+50 < 400):
                        captureList.append([piece.centerX-100, piece.centerY+100])
            if (bottomRightPiece in blackPieces): #if there's a piece to the right
                if (getPiece(bottomRightPiece.centerX+50, bottomRightPiece.centerY+50) == None):
                    if (bottomRightPiece.centerX+50 < 400 and bottomRightPiece.centerY+50 < 400):
                        captureList.append([piece.centerX+100, piece.centerY+100])
        
    else: #it's black's turn
        leftPiece = getPiece(piece.centerX-50, piece.centerY+50)
        rightPiece = getPiece(piece.centerX+50, piece.centerY+50)
        
        if (leftPiece in whitePieces): #if there's a piece to the left
            if (getPiece(leftPiece.centerX-50, leftPiece.centerY+50) == None): #if there's no piece further ahead
                if (leftPiece.centerX-50 > 0 and leftPiece.centerY+50 < 400):
                    captureList.append([piece.centerX-100, piece.centerY+100])
        if (rightPiece in whitePieces): #if there's a piece to the right
            if (getPiece(rightPiece.centerX+50, rightPiece.centerY+50) == None):
                if (rightPiece.centerX+50 < 400 and rightPiece.centerY+50 < 400):
                    captureList.append([piece.centerX+100, piece.centerY+100])
        if (piece.king):
            upperLeftPiece = getPiece(piece.centerX-50, piece.centerY-50)
            upperRightPiece = getPiece(piece.centerX+50, piece.centerY-50)
            
            if (upperLeftPiece in whitePieces): #if there's a white piece to the left
                if (getPiece(upperLeftPiece.centerX-50, upperLeftPiece.centerY-50) == None): #if there's no piece in the way
                    if (upperLeftPiece.centerX-50 > 0 and upperLeftPiece.centerY-50 > 0):
                            captureList.append([piece.centerX-100, piece.centerY-100])
            if (upperRightPiece in whitePieces): #if there's a white piece to the right
                if (getPiece(upperRightPiece.centerX+50, upperRightPiece.centerY-50) == None):
                    if (upperRightPiece.centerX+50 < 400 and upperRightPiece.centerY-50 > 0):
                            captureList.append([piece.centerX+100, piece.centerY-100])
            
    return captureList
    
def projectMoves(piece):
    if (app.turn):
        if (captures(piece)):
            for coords in captures(piece):
                app.moves.append(Circle(coords[0], coords[1], 20, fill='white', opacity=75))
        else:
            if (getPiece(piece.centerX+50, piece.centerY-50) == None):
                app.moves.append(Circle(piece.centerX+50, piece.centerY-50, 20, fill='white', opacity=75))
            if (getPiece(piece.centerX-50, piece.centerY-50) == None):
                app.moves.append(Circle(piece.centerX-50, piece.centerY-50, 20, fill='white', opacity=75))
            if (piece.king):
                if (getPiece(piece.centerX+50, piece.centerY+50) == None):
                    app.moves.append(Circle(piece.centerX+50, piece.centerY+50, 20, fill='white', opacity=75))
                if (getPiece(piece.centerX-50, piece.centerY+50) == None):
                    app.moves.append(Circle(piece.centerX-50, piece.centerY+50, 20, fill='white', opacity=75))
    else:
        if (captures(piece)):
            for coords in captures(piece):
                app.moves.append(Circle(coords[0], coords[1], 20, fill='darkslategrey', opacity=75))
        else:
            if (getPiece(piece.centerX+50, piece.centerY+50) == None):
                app.moves.append(Circle(piece.centerX+50, piece.centerY+50, 20, fill='darkslategrey', opacity=75))
            if (getPiece(piece.centerX-50, piece.centerY+50) == None):
                app.moves.append(Circle(piece.centerX-50, piece.centerY+50, 20, fill='darkslategrey', opacity=75))
            if (piece.king):
                if (getPiece(piece.centerX+50, piece.centerY-50) == None):
                    app.moves.append(Circle(piece.centerX+50, piece.centerY-50, 20, fill='darkslategrey', opacity=75))
                if (getPiece(piece.centerX-50, piece.centerY-50) == None):
                    app.moves.append(Circle(piece.centerX-50, piece.centerY-50, 20, fill='darkslategrey', opacity=75))

def selectPiece(piece):
    piece.border = 'green'
    app.selection = piece
    projectMoves(piece)
    app.clicks += 1

def deletePiece(piece):
    try:
       whitePieces.remove(piece)
    except:
        blackPieces.remove(piece)
    app.group.remove(piece)
    
def movePiece(piece, selectMove):
    piece.centerX = selectMove.centerX
    piece.centerY = selectMove.centerY
    piece.toFront()
    for item in app.moves:
        app.group.remove(item)
    app.moves.clear()
    app.clicks += 1
    
def captureMove(move):
    midX = (move.centerX + app.selection.centerX) / 2 #midpoint of x-values
    midY = (move.centerY + app.selection.centerY) / 2 #midpoint of y-values
    capturedPiece = getPiece(midX, midY)
    deletePiece(capturedPiece)
    movePiece(app.selection, move)
    if (len(captures(app.selection)) == 0):
        app.canCapture = False

def cleanup():
    if (len(blackPieces) == 0 or len(whitePieces) == 0): #check if any side has no pieces
        app.win = True #if so, somebody has won
    
    #king any checkers that are on the opposing back row
    for piece in whitePieces:
        if (piece.centerY < 50):
            piece.king = True
            piece.fill = gradient('white', 'white', 'black', 'white', 'white')
    for piece in blackPieces:
        if (piece.centerY > 350):
            piece.king = True
            piece.fill = gradient('darkslategrey', 'darkslategrey', 'black', 'darkslategrey', 'darkslategrey')
    
    #reset tracking variables
    app.clicks = 0
    app.canCapture = False
    app.moves.clear()
    app.selection = None
    
    #pass the turn
    if (app.turn):
        for piece in whitePieces:
            piece.border = None
        #if it was white's turn, it's now black's turn
        app.turn = False
        print("Black's Turn")
    else:
        for piece in blackPieces:
            piece.border = None
        #if it was black's turn, it's now white's turn
        app.turn = True
        print("White's Turn")

print("White's Turn")
def onMousePress(mouseX,mouseY):
    if (app.win == False):
        if (app.turn): #if it's white's turn
            #check if you can capture, because it changes the behavior of actions
        
            if (app.clicks == 0): #if you haven't made a valid piece selection
                for piece in whitePieces:
                    if (captures(piece)):
                        app.canCapture = True
                        piece.border = 'yellow'
                if (getPiece(mouseX, mouseY) in whitePieces):
                    if (app.canCapture):
                        if (captures(getPiece(mouseX, mouseY))): #if the piece selected has a valid capturing move
                            selectPiece(getPiece(mouseX, mouseY))
                    
                        else:
                            getPiece(mouseX, mouseY).border = 'red'
                
                    else:
                        selectPiece(getPiece(mouseX, mouseY))
                    
            elif (app.clicks == 1): #if you've selected a piece, but haven't moved it
                if (getPiece(mouseX, mouseY) in app.moves): #you need to select a move
                    if (app.canCapture):
                        captureMove(getPiece(mouseX, mouseY))
                    else:
                        movePiece(app.selection, getPiece(mouseX, mouseY))
        
            elif (app.canCapture):
                if (app.clicks % 2): #if the number of clicks is odd
                    if (getPiece(mouseX, mouseY) in app.moves):
                        captureMove(getPiece(mouseX, mouseY))
                
                else: #if the number of clicks is even
                    if (getPiece(mouseX, mouseY) == app.selection):
                        selectPiece(app.selection)
                    
                    else:
                        for piece in whitePieces:
                            if piece != app.selection:
                                piece.border = None
                        if (getPiece(mouseX, mouseY)):
                            getPiece(mouseX, mouseY).border = 'red'
                        app.selection.border = 'yellow'
        
            else:
                cleanup()
        
        # now it's black's turn
        else:
            if (app.clicks == 0):
                for piece in blackPieces:
                    if (captures(piece)):
                        app.canCapture = True
                        piece.border = 'yellow'
                if (getPiece(mouseX, mouseY) in blackPieces):
                    if (app.canCapture):
                        if (captures(getPiece(mouseX, mouseY))):
                            selectPiece(getPiece(mouseX, mouseY))
                        else:
                            getPiece(mouseX, mouseY).border = 'red'
                    else:
                        selectPiece(getPiece(mouseX, mouseY))
        
            elif (app.clicks == 1):
                if (getPiece(mouseX, mouseY) in app.moves):
                    if (app.canCapture):
                        captureMove(getPiece(mouseX, mouseY))
                    else:
                        movePiece(app.selection, getPiece(mouseX, mouseY))
            
            elif (app.canCapture):
                if (app.clicks % 2):
                    if (getPiece(mouseX, mouseY) in app.moves):
                        captureMove(getPiece(mouseX, mouseY))
                    
                else:
                    if (getPiece(mouseX, mouseY) == app.selection):
                        selectPiece(app.selection)
                    else:
                        for piece in blackPieces:
                            if piece != app.selection:
                                piece.border = None
                        if (getPiece(mouseX, mouseY)):
                            getPiece(mouseX, mouseY).border = 'red'
                        app.selection.border = 'yellow'
        
            else:
                cleanup()
    else:
        print("GAME OVER")
        if (len(whitePieces)):
            print("White won the game!")
            Label("White Wins!", 200, 200, fill='crimson', size=60, bold=True)
        else:
            print("Black won the game!")
            Label("Black Wins!", 200, 200, fill='crimson', size=60, bold=True)
        app.stop()

def onKeyPress(key):
    #press space to cancel a selection
    if (key == 'space' and app.clicks == 1):
        app.clicks -= 1
        if (app.turn):
            for piece in whitePieces:
                if (piece != app.selection):
                    piece.border = None
                else:
                    #deselect the piece
                    piece.border = None
                    app.selection = None
                    for move in app.moves:
                        app.group.remove(move)
                    app.moves.clear()
            
        else:
            for piece in blackPieces:
                if (piece != app.selection):
                    piece.border = None
                else:
                    piece.border = None
                    app.selection = None
                    for move in app.moves:
                        app.group.remove(move)
                    app.moves.clear()

cmu_graphics.run()