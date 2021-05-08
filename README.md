# RoPaSci360-B
**TO DO:**
- consider data representation of the board for optimal searching (pending)
- consider evaluation function (possible use of machine learning here)
- research minimax algorithm and how to extend it to simultaneous play
- optimize the program to improve time complexity
- work on weights for the evaluation function
- increase depth of the search tree

**IDEAS**
- Player class has attribute 'Move Strategy'
    - 'Move' strategy is abstract class implemented by concrete strategies
    - allows for strategy to be switched dynamically
    - possible application of this: record moves of opponent and if we note that they are \
      always choosing the minimum utility move from move matrix, then alter our strategy to \
      abuse this
      
- Evaluation function considers:
    - upper rocks / lower scissors + upper papers / lower rocks + upper scissors / lower papers
        - other way round for if we are playing lower instead of upper
    - total distance from upper rocks to lower scissors + total distance from upper papers \
      to lower rocks + total distance from upper scissors to lower papers
      
    - number of upper tokens - number of lower tokens
      
- Always have 'Player' playing 'upper' internally and if it has been assigned 'lower' just \
  invert the moves given to the referee and invert the moves coming from the referee
  
- Have a token run away if things are looking bad to guarantee draw

**IN THIS UPDATE**
- removed is_legal function, implement legal move generation on the fly to save time
- new feature which takes into account hexes with more than one token on them
    - idea being that it is bad to have, for example, 2 rocks on one hex as they can both
    be killed at once
      
- another new feature: difference in remaining throws
- added random player
- need to bugfix move generating; still generating illegal moves
