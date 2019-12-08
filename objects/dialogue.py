import constants as c
from re import search

class speechBlock():
    """A speechBlock object represents a block of speech for a
    non-player charcter."""
    label = ""
    speechText = []
    requiresResponse = False
    nextLines = []
    leaf = False                # if this line is a leaf in the dialogue
    speechType = None

    def __init__(self, newLabel, newSpeechText, newNextLines, newSpeechType):
        self.label = newLabel
        self.speechText = newSpeechText
        self.nextLines = newNextLines
        if len(self.nextLines) is 0:
            self.leaf = True
        self.speechType = newSpeechType

    def nextBlock(self, lineNumber):
        if lineNumber > len(self.nextLines):
            raise IndexError("Line number exceeded nextLines list size")
        else:
            return self.nextLines[lineNumber]

class PlayerLine():
    """A PlayerLine object represents a player dialogue choice."""
    playerOptions = []

    def getPlayerOptions(self):
        return playerOptions

class Dialogue():
    """A Dialogue is a tree of speechBlocks and represents a full dialogue
       interaction between the player and another character"""
    def __init__(self):
        """Parse dialogue file and construct dialogue tree based on dialogueTag"""
        self.dialogueList = []
        self.currentBlock = None
        self.next_block = 0

    def create_character_dialogue(self, dialogueTag, name):
        self.name = name

        dialogue_path = c.DIALOGUE_PATH_DICT[dialogueTag]

        with open(dialogue_path, 'r') as f:
            # readMode definition:
            # 0 - looking for TAG
            # 1 - looking for START
            # 2 - reading speech block, ends when END is reached
            # 3 - determining branch options
            readMode = 0

            currentTag = 1
            textBlock = []
            speechType = None
            for currentLine in f:
                if readMode is 0:
                    # Searches for TAG
                    if 'TAG' in currentLine:
                        if 'NPC' in currentLine:
                            speechType = 'NPC'
                        else:
                            speechType = 'PLAYER'
                        currentTag = [int(s) for s in currentLine.split() if s.isdigit()][0]
                        readMode = 1
                elif readMode is 1:
                    # Searches for START
                    if 'START' in currentLine:
                        readMode = 2
                elif readMode is 2:
                    # Stores Text until END
                    if 'END' in currentLine:
                        readMode = 3
                    else:
                        textBlock.append(currentLine.rstrip())
                elif readMode is 3:
                    # Records BRANCHES and creates speechBlock object
                    if 'BRANCHES' in currentLine:
                        branches = [int(s) for s in currentLine.split() if s.isdigit()]
                        if branches is not []:
                            newSpeechObject = speechBlock(currentTag,textBlock, branches, speechType)
                            self.dialogueList.append(newSpeechObject)
                        # Resets for next block
                        readMode = 0
                        textBlock = []

    def create_plant_dialogue(self, growth_stage):
        if growth_stage is 'DIRT'
            pass

    def set_next_block(self, option):
        print("test")
        self.next_block = option

    def do_dialogue(self):
        endDialogue = False
        self.currentBlock = self.dialogueList[0]

        while not endDialogue:
            yield self.currentBlock
            if self.currentBlock.speechType is 'NPC':
                print("EMILIA:")
                print(self.currentBlock.speechText)
                print()
                if not self.currentBlock.leaf:
                    self.currentBlock = self.dialogueList[self.currentBlock.nextBlock(0) - 1]
                else:
                    endDialogue = True
            else:
                print("YOU:")
                print(self.currentBlock.speechText)
                print()
                self.currentBlock = self.dialogueList[self.currentBlock.nextBlock(self.next_block-1) - 1]





