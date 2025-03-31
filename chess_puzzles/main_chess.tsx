import React, {useState} from "react";
import {View, Button, Text } from "react-native";
import {Chess} from "chess.js";

import Chessboard from "react-native-chessboard";

const puzzles = [
    {
      id: 1,
      fen: "8/8/8/8/8/5k2/6R1/6K1 w - - 0 1", // White to move and checkmate in 1
      solution: ["Rg8#"]
    },
    {
      id: 2,
      fen: "r1bqkb1r/pppp1ppp/2n2n2/4p3/4P3/3P4/PPP2PPP/RNBQKBNR w KQkq - 2 3",
      solution: ["d4"]
    }
  ];

const PuzzleScreen = () => {
    const [chess] = useState(new Chess(puzzles[0].fen));
    const [gameOver, setGameOver] = useState(false);

    const onMove = (move) => {
        if (chess.move(move)){
            if (puzzles[0].solution.includes(move.san)){
                setGameOver(true);
                alert("Correct! Puzzle solved.");
            } else {
                chess.undo()
                alert("Incorrect move. Try again.");
            }
        }
    };

    return (
        <View>
            <Text>Chess Puzzle</Text>
            <Chessboard fen={puzzles[0].fen} onMove={onMove} />
            {gameOver && <Button title="Next Puzzle" onPress={() => console.log("Next Puzzle")} />}
        </View>
    );
};

export default PuzzleScreen