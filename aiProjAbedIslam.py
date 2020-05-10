# 15 Puzzle
# Abed Islam ai1138
import copy;
########### This is all the object representations I needed for the project######################
#this is the board of the 15 puzzle game 
class Board :
    def __init__ (self, board, goal, blank_tup):
        self.board = board;
        self.goal = goal;
        self.blank_r = blank_tup[0]; 
        self.blank_c = blank_tup[1];
    #to see if a move can be made
    def move (self, direction):
        if direction == "L":
            if direction in self.legalMoves():
                self.board[self.blank_r][self.blank_c], self.board[self.blank_r][self.blank_c+1] = \
                    self.board[self.blank_r][self.blank_c+1], self.board[self.blank_r][self.blank_c];
                self.blank_c += 1;

        if direction == "R":
            if direction in self.legalMoves():
                self.board[self.blank_r][self.blank_c], self.board[self.blank_r][self.blank_c-1] = \
                    self.board[self.blank_r][self.blank_c-1], self.board[self.blank_r][self.blank_c];
                self.blank_c -= 1;

        if direction == "U":
            if direction in self.legalMoves():
                self.board[self.blank_r][self.blank_c], self.board[self.blank_r-1][self.blank_c] = \
                    self.board[self.blank_r-1][self.blank_c], self.board[self.blank_r][self.blank_c];
                self.blank_r -= 1;

        if direction == "D":
            if direction in self.legalMoves():
                self.board[self.blank_r][self.blank_c], self.board[self.blank_r+1][self.blank_c] = \
                    self.board[self.blank_r+1][self.blank_c], self.board[self.blank_r][self.blank_c];
                self.blank_r += 1;

        return self;

    def legalMoves(self):
        lml = [];
        if self.blank_c != 3:
            lml.append("L");
        if self.blank_c != 0:
            lml.append("R");
        if self.blank_r != 0:
            lml.append("U");
        if self.blank_r != 3:
            lml.append("D");
        return lml;

    def getBoard (self):
        return self.board;

    def getGoalBoard (self):
        return self.goal;

    def isSolved (self):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if (self.board[row][col] != self.goal[row][col]):
                    return False;
        return True;
     #this function shows the potential next board if a node or tile is shifted in a certain direction
    def predict(self,action):
        bdLst = copy.deepcopy(self.board)
        newBoard = Board(bdLst, self.goal, (self.blank_r, self.blank_c))
        newBoard.move(action);
        return newBoard;
        
    
    def __eq__(self, other):
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if (self.board[row][col] != other.board[row][col]):
                    return False;
        return True;
    
    def __repr__(self):
        string="State: "
        for i in range(4):
            string += "[ "
            for j in range(4):
                string += str(self.board[i][j]) +" ";
            if i == 3:
                string +="]"
            else:
                string +="] , "
        return string;


############################################################################
# the node class holds the board and the prediction of moves along with the huerstic 
class Node :
    def __init__ (self, data, parent = None, fn = None):
        self.data  = data
        self.parent = parent
        self.fn = fn

    def child(self, data):
        return Node(data,self)

    def sequence(self):
        node = self
        seq_to_node = []
        while node:
            seq_to_node.append(node)
            node = node.parent;
        return list(reversed(seq_to_node))

    def __repr__(self):
        string = "Node: \n"
        string += "\tData:\n"
        string += str(self.data)
        string += "\tf(n):\n"
        string += str(self.fn)
        return string

    def __eq__(self, other):
        if self.data == other.data:
            return True;
        return False;

    def fn(self, fn):
        self.fn = fn;
        return;
#the priotity queue is used to help in the astar search method
class PriorityQueue :
    def __init__ (self):
        self.data = [];
        self.values = [];
    
    def __find_min_index(self, lst):
        min = lst[0];
        min_index = 0;
        for i in range(1, len(lst)):
            if (lst[i] < min):
                min = lst[i];
                min_index = i;
        return min_index;

    def pop(self):
        min_index = self.__find_min_index(self.values);
        self.values.pop(min_index);
        data = self.data.pop(min_index);
        return data;

    def add(self, data, value):
        self.data.append(data);
        self.values.append(value);

    def hasNext(self):
        return self.data != []

    def contains(self, data):
        return data in self.data

    def getVal(self, data):
        data_index = self.data.index(data);
        return self.values[data_index];

    def remove (self, data):
        x = self.data.index(data);
        self.data.remove(data);
        self.values.pop(x);

    def size(self):
        return len(self.data);

    def __repr__(self):
        string = "\nPriorQ :\n"
        if (len(self.data) == 0):
            return string + "\tEmpty\n"
        for i in range(len(self.data)):
            if (i == (len(self.data) -1)):
                string +=  "\tdata: " + str(self.data[i]) + "\n"
                string += "\tvalue: " + str(self.values[i]) + "\n"
            else:
                string +=  "\tdata: " + str(self.data[i]) + "\n"
                string += "\tvalue: " + str(self.values[i]) + "\n\n"

        return string
############################################################################




#to get the start position of the puzzle
def getIndicies(val , board_lst):
    for row in range(len(board_lst)):
        for col in range(len(board_lst[row])):
            if (board_lst[row][col] == val) :
                return (row,col);

#calculate fn value for astar algorithm
def manhattanFunc(board):
    currState = board.getBoard();
    goalState = board.getGoalBoard();

    sums = 0
    for row in range(len( currState)):
        for col in range(len( currState[row])):
            if (currState[row][col] != 0):
                ind_curr =  (row,col)
                ind_goal =   getIndicies(currState[row][col], goalState)
                diff_x   = abs(ind_curr[0] - ind_goal[0])
                diff_y   =   abs(ind_curr[1] - ind_goal[1])
                sums    +=  diff_x
                sums   +=  diff_y
    return sums;

#the actual search algorithm
def aStar(board, heuristic): 
    lookFor = PriorityQueue();
    node = Node(board, None, heuristic(board));
    found = [];
    lookFor.add(node, heuristic(node.data) + (len(node.sequence()) - 1));
   
    while lookFor.hasNext():
        node = lookFor.pop();

        #checks if the node is the solution
        if node.data.isSolved():
            print("solved")
            return (node.sequence(), (len(found) + 1));


        #predicts next viable move
        for move in node.data.legalMoves():
            child = Node(node.data.predict(move), node);
            child.fn(heuristic(child.data) + len(child.sequence()) - 1)
         
            if (lookFor.contains(child)==False) and (child.data not in found):
                lookFor.add(child, (heuristic(child.data) + len(child.sequence()) - 1) );
            
            # child is in frontier
            elif frontier.contains(child):
               
                child_f_n = heuristic(child.data) + (len(child.sequence())-1);
                print(child_f_n < lookFor.getVal(child))
                if (child_f_n < lookFor.getVal(child)):
                    lookFor.remove(child);
                    child.fn(child_f_n);
                    lookFor.add(child, child_f_n);
                    
            
            
            found.append(node.data);
           
    
    
    return None, len(found)

# -----------------------------------------------------


#creates the sequence to solve the board
def findMoveSeq(board_seq_lst):
    
    coor_lst = [];
    for i in range(len(board_seq_lst)):
        coor_lst.append(getIndicies(0 , board_seq_lst[i]))
    #print(coor_lst)
    move_lst = []
    for i in range(len(coor_lst)-1):
        delta_row = coor_lst[i][0] - coor_lst[i+1][0]
        delta_col = coor_lst[i][1] - coor_lst[i+1][1]

        if delta_row == -1:
            move_lst.append("U")
        if delta_row == 1:
            move_lst.append("D")
        if delta_col == -1:
            move_lst.append("L")
        if delta_col == 1:
            move_lst.append("R")

    return move_lst;





# ----------------------------------------------------

#set up boards crom txt files
def get_init_and_goal_boards(file):
    init_board = []
    final_board = []
    counter = -1;
    f_lines = file.readlines()
    for i in f_lines:
        counter+=1;
        if counter < 4:
            init_board.append(i.strip().split(" "))

        elif (counter < 9) and (counter > 4):
            final_board.append(i.strip().split(" "))
    
    for i in range(4):
        init_board[i] = [int(i) for i in init_board[i]]
        final_board[i] = [int(i) for i in final_board[i]] 

    return (init_board, final_board )

#execute files
def main():
    # Read Input File
    fI = open("Input4.txt", "r")
    boardStart, boardEnd = get_init_and_goal_boards(fI)
    
    print(boardStart)
    print(boardEnd)
    # create Boards
    blank_tup = getIndicies(0, boardStart)
    board_prob = Board(boardStart, boardEnd, blank_tup)
    

    
    # Solve the puzzle
    seq, numExplored = aStar(board_prob, manhattanFunc)
    
    print("\nSolution Sequence: ")
    print("\tData:")
    for i in range(len(seq)):
        print("\t\t",seq[i].data)
    
    print("\tf(n):")
    for i in range(len(seq)):
        print("\t\t",seq[i].fn)
    
    print("\tMoves:")
    boardLst = []
    for i in range(len(seq)):
        boardLst.append(seq[i].data.getBoard())
    print(len(boardLst)) # 17 moves
    move_lst = findMoveSeq(boardLst)
    for i in range(len(move_lst)):
        print("\t\t", move_lst[i])

    print("\nNum Explored: ", numExplored,"\n")
    

main()