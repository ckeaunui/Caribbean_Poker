# Heads_Up_Caribbean_Poker
This is a version of Caribbean poker where the user plays against the house (computer).  The rules of this game are explained at the bottom.

Profile_data.csv is where all profile data is stored to preserve the users stats after the program has terminated. Data is automatically updated here as the user plays the game

Cards.csv stores the name, value, and suit of each card

Card.py is a Card object which stores the cards name, value, and suit (represented by a numerical value 1-4)

Profile.py is another object called Profile that is responsible for storing the users information. The users current balance, wins losses, and total buy in amount are all 
recorded, and then saved in Profile_data.csv.  This object contains several setter methods such as add_money() or updata_balance() which update the users profile data as they play

main.py is where the game is run.  First all profiles are read into a dictionary called all_profile_data, and then the user is prompted to sign in or create a new account.  
Once signed in they are prompted to select an 'ante' (initial bet amount),  If they can afford it the game will start, otherwise they will be prompted to add money to their
account.  When the game is in action, get_cards is called which randomly assigns the user, house, and table with random cards from Cards.csv, ensuring no duplicates are dealt.
If the user plays until the end of the round, all cards are revealed and then sent to get_showdown to get a numeric value repreenting the strength of their hand (more info 
below). After determining the best hand, a winner is picked and money is distributed accordingly.  The user is allowed to play until they decide to quit by entering 'q' after 
a round, or if they run out of money and refuse to add more.


Hand Showdown Value Breakdown:

  Each hands showdown value is represented by a decimal value, with the value before the decimal representing the group the users hand belongs to. 
  
    10 - Royal Flush
    9 - Straight Flush
    8 - Four of a Kind
    7 - Full House
    6 - Flush
    5 - Straight
    4 - Three of a kind
    3 - Two Pair
    2 - Pair
    1 - High Card

  The float then contains 10 decimal values, which represent the 5 cards the user has in order of importance.
  Ex.  A Full House with the 5 card values (10, 10, 10, 8, 8)  would be represented as 7.1010100808, with the 7 representing the full house classification, and the decimal
  representing 3 10's and 2 8's. which is the strength of the users Full House.  If the user has this showdown and the computer has 7.1010100303, the computer also has a 
  Full House, but because their pair of 3's are weaker than the users pair of 8's the computer loses.


RULES (Copied from 'howtoplay.org'):
https://www.howtoplay.org/caribbean-holdem/

  1. Placing an Ante Bet:
    The game begins when you place a mandatory ante bet, and this can be any amount you choose depending on your bankroll limitations. Many players enjoy Caribbean Hold’em 
    Poker for just $1 per hand, while others like to bump the action up to $5 or $10 per hand or even more.

  2. Dealing the Cards:
    After you’ve made the ante wager, an action performed by simply clicking the chip amounts you’d like to bet, clicking deal will cause the dealer to distribute two cards 
    face up to form your hand, and two cards face down to form their own hand.

  3. Check if you Won Against the Dealer:
    Finally, the dealer will place three cards face up in the middle of the table, and just like traditional Texas Hold’em Poker, these crucial community cards are known as 
    the flop.
    

  Winning at Caribbean Hold’em
  
    The objective of Caribbean Hold’em Poker is to form the best five-card poker hand, by combining either one or both of your two hole cards with the community cards on board. 
    For example, if you ante up and are dealt an ace and king, while the flop comes down queen jack-ten, this five-card combination gives you the Broadway straight.

    A more likely scenario, however, would see you receive something like a queen and ten, with one more ten arriving on the flop. In this case, you’ve made a pair of tens at 
    minimum, with the chance to improve your hand on the arrival of the next two community cards.  Those two cards can only hit the felt in certain conditions though, and this 
    forms the basis of Caribbean Hold’em Poker as a game of practice and strategy.

    After you ante up and take a look at your two hole cards, along with the flop, the time has come for you to make a choice: you can either fold (when your two cards fail to 
    connect with the flop) while surrendering your ante bet, or you can call and see the next two community cards. In order to call, you must place an additional wager equal to 
    exactly twice the amount of your ante bet.

    So, if you’ve decided on an ante bet of $5, and you like the look of your hand after the flop, calling to play the hand out will cost you $10 more for a total wager of $15. 
    On the other hand, if your hole cards are marginal and you’d rather move on to the next hand, folding and surrendering simply costs you the ante bet.


  Simplified:
  
    1. Ante Bet: A new hand of Caribbean Hold’em Poker begins with an ante wager. Place this in the circle marked “Ante”.
    
    2. Progressive Side Bet: The player also decides to make the progressive side bet or not. This is a blind bet, with no knowledge of your hand.
    
    3. The Deal: The player and the dealer each receive two hole cards. Next, the dealer deals out 3 community cards — the flop.
    
    4. Call Bet: After the flop, the player must decide to make the call bet or not. The call bet must be two times the ante bet. If this bet isn’t made, the player loses 
       the ante bet.
    
    5. Turn & River: Next, the dealer deals out two more community cards, which would be called the turn and river cards in Texas Hold’em.
    
    6. Best 5-Card Hand: Using your two hole cards and the five community cards, you must make the best 5-card hand. The dealer does the same.
    
    7. Dealer Qualifies: Before hands are compared, the dealer must qualify. To do this, the dealer must have a pair of 4s or better. If the dealer fails to qualify, the 
       player wins 1:1 on the ante bet. The call bet is a push.
    
    8. Winnings Paid: If the dealer qualifies, then the hands are compared. If the dealer wins, the player loses the ante and call bets. If the player wins, he or she 
       wins according to the ante bet pay table, while winning 1:1 on the call bet.
    
    9. Progressive Payouts: If the player wins according to the progressive side bet’s payout table, these winnings are paid to the player.
    

