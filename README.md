# Chess Engine

A Python chess engine and interactive GUI built from scratch using bitboard representations and magic bitboard move generation.

## About

This is a passion project to learn more about the inner workings of how chess engines work. The goal is to also develop a ML chess engine to learn more about creating and designing ML models.

## Project Structure

```
chess-engine/
├── movegen.py          # Attack generation for all piece types
├── play.py             # pygame-ce window, drawing loop, click handling
├── logic/
│   ├── movegen.py      # Attack generation for all piece types
│   └── board.py        # Board state, bitboard helpers, piece definitions  
└── assets/             # Piece PNG images
```

## Requirements

- Python 3.14+

## Installation

```bash
git clone https://github.com/Grant-Sooy/Chess-Engine.git
cd Chess-Engine
pip install -e .
```

## Running

```bash
python play.py
```
