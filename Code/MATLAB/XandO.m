classdef XandO
% The class creates the noughts and crosses game 
%
% How to Play:
% Press F5 to run the program, the computer will always be 'O' and the 
% player will always be 'X'. For the player to make a move type:
% ans.move(position) where position is a number between 1 and 9 inclusive
% For the computer to make a move type: ans.computerMove

    
    properties
        board
    end
    
    methods
        % Creates the board
        % Constructor Function
        function Game = XandO
            Game.board = '         ';
        end
        
        % Display function
        function disp(Game)
            disp([Game.board(1) ' | ' Game.board(2) ' | ' Game.board(3);
                '--|---|--';
                Game.board(4) ' | ' Game.board(5) ' | ' Game.board(6);
                '--|---|--';
                Game.board(7) ' | ' Game.board(8) ' | ' Game.board(9)])
        end
        
        % Check if a move is valid
        function check = legalMoves(a)             
            check = strfind(a.board,' ');
        end
        
        % It handles the movement system for the player
        % and checks if the game is a draw
        function a = move(a,i)                 
            A = legalMoves(a);
            B = any(i == A);
            
            if (B == 1)
                a.board(i) = 'X';
                a.board = a.board;
                win(a)
            elseif all(a.board ~= ' ')
                disp('The game is a Draw')                
            else
                disp('The move is not legal')
                return 
            end
        end
        
        % Computer movement   
        function a = computerMove(a)            
            A = legalMoves(a);
            
            if length(A) > 1
                comp = randsample(A,1);
                a.board(comp) = 'O';
            elseif length(A) == 1
                comp = A(1,1);
                a.board(comp) = 'O';
            elseif all(a.board ~= ' ')
                disp('The game is a Draw!')
                return
            end
            
            a.board = a.board;
            win(a)
        end
        
        % It checks if the game is finished
        function win(a)         
            for j = 1:9
                if j == 1
                    if a.board(j) == 'X' && a.board(j+1) == 'X' && a.board(j+2) == 'X'
                        disp('The player Wins the game!')
                        return
                    elseif a.board(j) == 'O' && a.board(j+1) == 'O' && a.board(j+2) == 'O'
                        disp('The computer Wins the game!')
                        return
                    elseif a.board(j) == 'X' && a.board(j+3) == 'X' && a.board(j+6) == 'X'
                        disp('The player Wins the game!')
                        return
                    elseif a.board(j) == 'O' && a.board(j+3) == 'O' && a.board(j+6) == 'O'
                        disp('The computer Wins the game!')
                        return
                    elseif a.board(j) == 'X' && a.board(j+4) == 'X' && a.board(j+8) == 'X'
                        disp('The player Wins the game!')
                        return 
                    elseif a.board(j) == 'O' && a.board(j+4) == 'O' && a.board(j+8) == 'O'
                        disp('The computer Wins the game!')
                        return
                    end
                elseif j == 2
                    if a.board(j) == 'X' && a.board(j+3) == 'X' && a.board(j+6) == 'X'
                        disp('The player Wins the game!')
                        return 
                    elseif a.board(j) == 'O' && a.board(j+3) == 'O' && a.board(j+6) == 'O'
                        disp('The computer Wins the game!')
                        return
                    end
                elseif j == 3
                    if a.board(j) == 'X' && a.board(j+3) == 'X' && a.board(j+6) == 'X'
                        disp('The player Wins the game!')
                        return
                    elseif a.board(j) == 'O' && a.board(j+3) == 'O' && a.board(j+6) == 'O'
                        disp('The computer Wins the game!')
                        return
                    elseif a.board(j) == 'X' && a.board(j+2) == 'X' && a.board(j+4) == 'X'
                        disp('The player Wins the game!')
                        return
                    elseif a.board(j) == 'O' && a.board(j+2) == 'O' && a.board(j+4) == 'O'
                        disp('The computer Wins the game!')
                        return
                    end
                elseif j == 4
                    if a.board(j) == 'X' && a.board(j+1) == 'X' && a.board(j+2) == 'X'
                        disp('The player Wins the game!')
                        return
                    elseif a.board(j) == 'O' && a.board(j+1) == 'O' && a.board(j+2) == 'O'
                        disp('The computer Wins the game!')
                        return 
                    end
                elseif j == 7
                    if a.board(j) == 'X' && a.board(j+1) == 'X' && a.board(j+2) == 'X'
                        disp('The player Wins the game!')
                        return
                    elseif a.board(j) == 'O' && a.board(j+1) == 'O' && a.board(j+2) == 'O'
                        disp('The computer Wins the game!')
                        return
                    end
                end
            end
        end
        
    end
    
end




