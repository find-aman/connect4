from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.sessions.backends.db import SessionStore
from .models import MovesData
from .serializers import Moves


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
                s = SessionStore()
                s["board"] = board
                s["rowCount"] = rowCount
                s["turnCount"] = turnCount
                s["state"] = "READY"
                s.create()
                key = s.session_key
            else:
                state = "Invalid"
                data = {"state": state, "key": None}
                return Response(data)
            state = "READY"
            data = {"state": state, "key": key}
            return Response(data)
        except:
            state = "Invalid"
            data = {"state": state, "key": None}
            return Response(data)


class PlayGame(APIView):
    def get(self, request, *args, **kwargs):
        key = request.COOKIES["sessionid"]
        qs = MovesData.objects.filter(key=key)
        serializer = Moves(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        def checkWin(request):
            try:
                parameters = request.query_params
                column = parameters.get("column")
                colVal = int(column[0]) - 1
                rowCount = request.session["rowCount"]
                rowVal = rowCount[int(column[0]) - 1] - 1
                board = request.session["board"]
                state = request.session["state"]
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
                data = {
                    "state": state,
                    "move": None,
                    "winStatus": None,
                    "data": board,
                }
                return data

        def addMove(request):
            try:
                parameters = request.query_params
                colVal = int(parameters.get("column")[0])
                board = request.session["board"]
                state = request.session["state"]
                rowCount = request.session["rowCount"]
                turnCount = request.session["turnCount"]
                if rowCount[colVal - 1] == 0:
                    rowCount[colVal - 1] += 1
                    request.session["rowCount"] = rowCount
                    if turnCount % 2 == 0:
                        board[0][colVal - 1] = "Y"
                        request.session["board"] = board
                    else:
                        board[0][colVal - 1] = "R"
                        request.session["board"] = board
                else:
                    if turnCount % 2 == 0:
                        board[rowCount[colVal - 1]][colVal - 1] = "Y"
                        request.session["board"] = board
                    else:
                        board[rowCount[colVal - 1]][colVal - 1] = "R"
                        request.session["board"] = board
                    rowCount[colVal - 1] += 1
                    request.session["rowCount"] = rowCount
                data = {
                    "state": state,
                    "move": "Valid",
                    "winStatus": None,
                    "data": board,
                }
                turnCount += 1
                request.session["turnCount"] = turnCount
                return data
            except Exception as e:
                return str(e)

        def checkValid(request):
            parameters = request.query_params
            column = parameters.get("column")[0]
            player = parameters.get("player")
            turnCount = request.session["turnCount"]
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
            state = request.session["state"]
            board = request.session["board"]
            parameters = request.query_params
            column = parameters.get("column")
            player = parameters.get("player")
        except:
            return Response({"state": "STOP", "move": None, "winStatus": None, "data": None})
        if state == "READY":
            if checkValid(request):
                data = addMove(request)
                winStatus = checkWin(request)
                if winStatus == "R WIN":
                    data["winStatus"] = "Red WIN"
                    state = "STOP"
                    data["state"] = state
                    request.session["state"] = state
                elif winStatus == "Y WIN":
                    data["winStatus"] = "Yellow WIN"
                    state = "STOP"
                    data["state"] = state
                    request.session["state"] = state
                values = MovesData(key = request.COOKIES["sessionid"],move = "Valid",column = column[0],player = player,state = request.session["state"],winstatus=winStatus)
                values.save()

                return Response(data)
            else:
                values = MovesData(key = request.COOKIES["sessionid"],move = "Invalid",column = column[0],player = player,state = request.session["state"],winstatus=None)
                values.save()
                return Response(
                    {"state": state, "move": "Invalid", "winSatus": None, "data": board}
                )
            
        else:
            return Response({"state": state, "move": "None", "winSatus": None, "data": board})
