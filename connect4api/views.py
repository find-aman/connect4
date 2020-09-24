from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import string

board = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]
rowCount = [0, 0, 0, 0, 0, 0, 0]
turnCount = 0
state = "STOP"


class Game(APIView):
    def get(self, request, *args, **kwargs):
        global board, rowCount, turnCount, state
        try:
            parameters = request.query_params
            if parameters["state"].upper() == "START":
                board = [
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                ]
                rowCount = [0, 0, 0, 0, 0, 0, 0]
                turnCount = 0
                request.session["board"] = board
                request.session["rowCount"] = rowCount
                request.session["turnCount"] = turnCount
                request.session["state"] = "READY"
            else:
                state = "Invalid"
                data = {"state": state, "comment": "Invalid Parameter Value"}
                return Response(data)
            state = "READY"
            data = {"state": state, "comment": "Game has been reset"}
            return Response(data)
        except:
            state = "Invalid"
            data = {"state": state, "comment": "Invalid Request"}
            return Response(data)


class PlayGame(APIView):
    def post(self, request, *args, **kwargs):
        def checkWin(board, rowVal, colVal):
            try:
                if (colVal + 3) < 7:
                    if (
                        board[rowVal][colVal + 0]
                        == board[rowVal][colVal + 1]
                        == board[rowVal][colVal + 2]
                        == board[rowVal][colVal + 3]
                    ):
                        if board[rowVal][colVal] == "Y":
                            return "Y WIN"
                        elif board[rowVal][colVal] == "R":
                            return "R WIN"

                if (colVal - 3) >= 0:
                    if (
                        board[rowVal][colVal - 0]
                        == board[rowVal][colVal - 1]
                        == board[rowVal][colVal - 2]
                        == board[rowVal][colVal - 3]
                    ):
                        if board[rowVal][colVal] == "Y":
                            return "Y WIN"
                        elif board[rowVal][colVal] == "R":
                            return "R WIN"

                if (rowVal + 3) < 6:
                    if (
                        board[rowVal + 0][colVal]
                        == board[rowVal + 1][colVal]
                        == board[rowVal + 2][colVal]
                        == board[rowVal + 3][colVal]
                    ):
                        if board[rowVal][colVal] == "Y":
                            return "Y WIN"
                        elif board[rowVal][colVal] == "R":
                            return "R WIN"

                if (rowVal - 3) >= 0:
                    if (
                        board[rowVal - 0][colVal]
                        == board[rowVal - 1][colVal]
                        == board[rowVal - 2][colVal]
                        == board[rowVal - 3][colVal]
                    ):
                        if board[rowVal][colVal] == "Y":
                            return "Y WIN"
                        elif board[rowVal][colVal] == "R":
                            return "R WIN"

                if (rowVal + 3) < 6 and (colVal + 3) < 6:
                    if (
                        board[rowVal + 0][colVal + 0]
                        == board[rowVal + 1][colVal + 1]
                        == board[rowVal + 2][colVal + 2]
                        == board[rowVal + 3][colVal + 3]
                    ):
                        if board[rowVal][colVal] == "Y":
                            return "Y WIN"
                        elif board[rowVal][colVal] == "R":
                            return "R WIN"

                if (rowVal - 3) >= 0 and (colVal - 3) >= 0:
                    if (
                        board[rowVal - 0][colVal - 0]
                        == board[rowVal - 1][colVal - 1]
                        == board[rowVal - 2][colVal - 2]
                        == board[rowVal - 3][colVal - 3]
                    ):
                        if board[rowVal][colVal] == "Y":
                            return "Y WIN"
                        elif board[rowVal][colVal] == "R":
                            return "R WIN"

                if (rowVal + 3) < 6 and (colVal - 3) >= 0:
                    if (
                        board[rowVal + 0][colVal - 0]
                        == board[rowVal + 1][colVal - 1]
                        == board[rowVal + 2][colVal - 2]
                        == board[rowVal + 3][colVal - 3]
                    ):
                        if board[rowVal][colVal] == "Y":
                            return "Y WIN"
                        elif board[rowVal][colVal] == "R":
                            return "R WIN"

                if (rowVal - 3) >= 0 and (colVal + 3) < 6:
                    if (
                        board[rowVal - 0][colVal + 0]
                        == board[rowVal - 1][colVal + 1]
                        == board[rowVal - 2][colVal + 2]
                        == board[rowVal - 3][colVal + 3]
                    ):
                        if board[rowVal][colVal] == "Y":
                            return "Y WIN"
                        elif board[rowVal][colVal] == "R":
                            return "R WIN"
            except:
                return "Invalid Request"

        def addMove(request, rowCount, columnValue):
            try:
                global turnCount
                parameters = request.query_params
                columnValue = int(parameters["column"])
                if rowCount[columnValue - 1] == 0:
                    rowCount[columnValue - 1] += 1
                    if turnCount % 2 == 0:
                        board[0][columnValue - 1] = "Y"
                    else:
                        board[0][columnValue - 1] = "R"
                else:
                    if turnCount % 2 == 0:
                        board[rowCount[columnValue - 1]][columnValue - 1] = "Y"
                    else:
                        board[rowCount[columnValue - 1]][columnValue - 1] = "R"
                    rowCount[columnValue - 1] += 1
                data = {
                    "move": "Valid",
                    "winStatus": None,
                    "data": board,
                }
                turnCount += 1
                return data
            except:
                return "Invalid Request"

        def checkValid(column, player, state):
            returnVal = False
            if column is not None:
                if int(column) in [1, 2, 3, 4, 5, 6, 7]:
                    returnVal = True
                else:
                    returnVal = False

            if player is not None:
                if player.upper() == "RED" or player.upper() == "YELLOW":
                    if (
                        turnCount % 2 == 0
                        and player.upper() == "YELLOW"
                        or turnCount % 2 != 0
                        and player.upper() == "RED"
                    ):
                        returnVal = True
                    else:
                        returnVal = False
                else:
                    returnVal = False

            return returnVal

        try:
            parameters = request.query_params
            column = parameters.get("column")
            player = parameters.get("player")
            global state
        except:
            return Response({"state": "Invalid", "comment": "Invalid Request"})
        if state == "READY":
            if checkValid(column, player, state):
                data = addMove(request, rowCount, column)
                winStatus = checkWin(
                    board, rowCount[int(column[0]) - 1] - 1, int(column[0]) - 1
                )
                if winStatus == "R WIN":
                    data["winStatus"] = "R WIN"
                    state = "STOP"
                elif winStatus == "Y WIN":
                    data["winStatus"] = "Y WIN"
                    state = "STOP"
                return Response(data)
            else:
                return Response({"move": "Invalid", "board": board})
        else:
            return Response({"state": "STOP"})
