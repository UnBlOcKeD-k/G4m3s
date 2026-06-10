#!/usr/bin/env python3
"""
Chess Game with GUI and Drag-and-Drop Interface
"""

import tkinter as tk
from tkinter import messagebox
from enum import Enum


class PieceType(Enum):
    PAWN = 1
    ROOK = 2
    KNIGHT = 3
    BISHOP = 4
    QUEEN = 5
    KING = 6


class Piece:
    """Represents a chess piece"""
    def __init__(self, color, piece_type):
        self.color = color  # 'white' or 'black'
        self.piece_type = piece_type  # PieceType enum
    
    def get_symbol(self):
        """Get Unicode symbol for the piece"""
        symbols = {
            (PieceType.PAWN, 'white'): '♙',
            (PieceType.ROOK, 'white'): '♖',
            (PieceType.KNIGHT, 'white'): '♘',
            (PieceType.BISHOP, 'white'): '♗',
            (PieceType.QUEEN, 'white'): '♕',
            (PieceType.KING, 'white'): '♔',
            (PieceType.PAWN, 'black'): '♟',
            (PieceType.ROOK, 'black'): '♜',
            (PieceType.KNIGHT, 'black'): '♞',
            (PieceType.BISHOP, 'black'): '♝',
            (PieceType.QUEEN, 'black'): '♛',
            (PieceType.KING, 'black'): '♚',
        }
        return symbols.get((self.piece_type, self.color), '?')


class ChessBoard:
    """Represents the chess board and game state"""
    
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = 'white'
        self.setup_board()
    
    def setup_board(self):
        """Initialize the board with starting positions"""
        # Set up white pieces (bottom, row 6-7)
        for col in range(8):
            self.board[6][col] = Piece('white', PieceType.PAWN)
        
        white_back_row = [
            PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP, PieceType.QUEEN,
            PieceType.KING, PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK
        ]
        for col, piece_type in enumerate(white_back_row):
            self.board[7][col] = Piece('white', piece_type)
        
        # Set up black pieces (top, row 0-1)
        for col in range(8):
            self.board[1][col] = Piece('black', PieceType.PAWN)
        
        black_back_row = [
            PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP, PieceType.QUEEN,
            PieceType.KING, PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK
        ]
        for col, piece_type in enumerate(black_back_row):
            self.board[0][col] = Piece('black', piece_type)
    
    def get_piece(self, row, col):
        """Get piece at position"""
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None
    
    def move_piece(self, from_row, from_col, to_row, to_col):
        """Move a piece from one position to another"""
        if not (0 <= from_row < 8 and 0 <= from_col < 8 and 
                0 <= to_row < 8 and 0 <= to_col < 8):
            return False
        
        piece = self.board[from_row][from_col]
        
        if piece is None:
            return False
        
        if piece.color != self.current_player:
            return False
        
        # Move the piece
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        
        # Switch player
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        return True
    
    def is_valid_move(self, from_row, from_col, to_row, to_col):
        """Check if a move is valid (simplified - allows any move)"""
        piece = self.board[from_row][from_col]
        if piece is None or piece.color != self.current_player:
            return False
        return True


class ChessGUI:
    """GUI for chess game with drag-and-drop"""
    
    SQUARE_SIZE = 60
    BOARD_SIZE = 8
    
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Game - Drag and Drop")
        self.root.resizable(False, False)
        
        self.board = ChessBoard()
        self.selected_piece = None
        self.selected_pos = None
        self.dragging = False
        
        # Create canvas
        canvas_size = self.SQUARE_SIZE * self.BOARD_SIZE
        self.canvas = tk.Canvas(
            root,
            width=canvas_size,
            height=canvas_size,
            bg='white',
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        
        # Bind events
        self.canvas.bind('<Button-1>', self.on_mouse_down)
        self.canvas.bind('<B1-Motion>', self.on_mouse_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_mouse_up)
        
        # Create info frame
        info_frame = tk.Frame(root)
        info_frame.pack(pady=10)
        
        self.info_label = tk.Label(
            info_frame,
            text=f"White's Turn",
            font=('Arial', 14, 'bold')
        )
        self.info_label.pack()
        
        reset_button = tk.Button(
            info_frame,
            text="New Game",
            command=self.reset_game,
            font=('Arial', 10)
        )
        reset_button.pack(pady=5)
        
        self.draw_board()
    
    def draw_board(self):
        """Draw the chess board"""
        self.canvas.delete('all')
        
        # Draw squares
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                x1 = col * self.SQUARE_SIZE
                y1 = row * self.SQUARE_SIZE
                x2 = x1 + self.SQUARE_SIZE
                y2 = y1 + self.SQUARE_SIZE
                
                # Alternate colors
                color = '#F0D9B5' if (row + col) % 2 == 0 else '#B58863'
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')
        
        # Highlight selected piece
        if self.selected_pos:
            row, col = self.selected_pos
            x1 = col * self.SQUARE_SIZE
            y1 = row * self.SQUARE_SIZE
            x2 = x1 + self.SQUARE_SIZE
            y2 = y1 + self.SQUARE_SIZE
            self.canvas.create_rectangle(x1, y1, x2, y2, outline='yellow', width=3)
        
        # Draw pieces
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                piece = self.board.get_piece(row, col)
                if piece:
                    self.draw_piece(piece, row, col)
    
    def draw_piece(self, piece, row, col, drag_offset=None):
        """Draw a piece on the board"""
        x = col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
        y = row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2
        
        if drag_offset:
            x += drag_offset[0]
            y += drag_offset[1]
        
        self.canvas.create_text(
            x, y,
            text=piece.get_symbol(),
            font=('Arial', 40),
            fill='black'
        )
    
    def on_mouse_down(self, event):
        """Handle mouse down event"""
        col = event.x // self.SQUARE_SIZE
        row = event.y // self.SQUARE_SIZE
        
        if 0 <= row < 8 and 0 <= col < 8:
            piece = self.board.get_piece(row, col)
            if piece and piece.color == self.board.current_player:
                self.selected_piece = piece
                self.selected_pos = (row, col)
                self.dragging = True
                self.draw_board()
    
    def on_mouse_drag(self, event):
        """Handle mouse drag event"""
        if self.dragging and self.selected_pos:
            self.draw_board()
            
            # Draw piece being dragged
            row, col = self.selected_pos
            drag_offset = (
                event.x - (col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2),
                event.y - (row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2)
            )
            
            # Redraw all pieces except the one being dragged
            for r in range(self.BOARD_SIZE):
                for c in range(self.BOARD_SIZE):
                    if (r, c) != self.selected_pos:
                        piece = self.board.get_piece(r, c)
                        if piece:
                            self.draw_piece(piece, r, c)
            
            # Draw dragged piece
            self.draw_piece(self.selected_piece, row, col, drag_offset)
    
    def on_mouse_up(self, event):
        """Handle mouse up event"""
        if not self.dragging or not self.selected_pos:
            return
        
        # Get target square
        target_col = event.x // self.SQUARE_SIZE
        target_row = event.y // self.SQUARE_SIZE
        
        from_row, from_col = self.selected_pos
        
        # Try to move the piece
        if (0 <= target_row < 8 and 0 <= target_col < 8 and 
            (target_row, target_col) != self.selected_pos):
            
            if self.board.is_valid_move(from_row, from_col, target_row, target_col):
                success = self.board.move_piece(from_row, from_col, target_row, target_col)
                if success:
                    self.update_info()
        
        self.dragging = False
        self.selected_piece = None
        self.selected_pos = None
        self.draw_board()
    
    def update_info(self):
        """Update the info label"""
        player = self.board.current_player.capitalize()
        self.info_label.config(text=f"{player}'s Turn")
    
    def reset_game(self):
        """Start a new game"""
        self.board = ChessBoard()
        self.selected_piece = None
        self.selected_pos = None
        self.dragging = False
        self.update_info()
        self.draw_board()


def main():
    root = tk.Tk()
    gui = ChessGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
