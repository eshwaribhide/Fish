## Self-Evaluation Form for Milestone 1

### General 

We will run self-evaluations for each milestone this semester.  The
graders will evaluate them for accuracy and completeness.

Every self-evaluation will go out into your Enterprise GitHub repo
within a short time afrer the milestone deadline, and you will have 24
hours to answer the questions and push back a completed form.

This one is a practice run to make sure you get


### Specifics 


- does your analysis cover the following ideas:
    - the need for an explicit Interface specification between the (remote) AI 
    players and the game system?
        
        - **"It will also help connect the AI player’s software to the Fish game" (refers to the logic layer)
        Lines 30-31.**
           
       - **In these lines, we are referring to how the logic layer basically coordinates all communication, including any communication that is needed between an AI Player and the Fish game/game server.**
       
    - the need for a referee sub-system for managing individual games
    
        - **In the lines below, we describe how the logic layer can behave as a referee.**
        
        - **"The logic layer also controls the game itself and can be thought of as the “referee”. 
        It determines the board layout and uses the data layer’s set of rules to make sure that 
        valid moves are being made."
        Lines 26-28**
     
     - the need for a tournament management sub-system for grouping players into games and dispatching to referee 
      components
      
       - **"This layer coordinates all aspects of the server and game and makes sure that everything is 
        running smoothly."
        Lines 22-23**
            
        - **In this statement, we implied that all aspects related to the server, which include sectioning off
        players into games, are handled by the logic layer.**

- does your building plan identify concrete milestones with demo prototypes:
    
    - for running individual games
  
        - **"Stage 2-Get Fish Game Working". (Paragraph 2)**
        
         - **This section details this component. We have an explicit statement here that
         "Then, the game board is rendered and the game will be played manually by the 4 players". We described
         how we basically wanted the game board and game functionality to be possible and for manual playing to
         be possible. (Paragraph 2, Sentence 3)**
         
     - for running complete tournaments on a single computer 
 
       - **"Stage 3– Get Fish Game Working with self-built AI players" (Paragraph 3)**
       
       -  **Here, we describe that we will make 4 AI players ourselves (4 is the max # of players) all with
        different strategies because 4 different hackers, in the real world, will probably have 4 different
        strategies in their algorithms. We don't explicitly mention anything here about a server and intended
        that this would be like a "practice run", having AI players that we built, and run the tournament
        on one computer.**
        
        - **"We need to find a way to hook these players up and integrate these players’ software into the 
        system, getting the AI software to interact with our general Fish game software, which will be handled 
        by the logic component." (Paragraph 3, Sentence 2)**
        
        - **In this sentence, we intended that we are integrating AI players into our system but not necessarily
        doing it on a server.**
      
     - for running remote tournaments on a network
      
        - **"Stage 4– Get Fish Game Working with Hackers’ AI players"**
  
        - **"The data layer will need to store information about the hackers and the AI players/their software. The logic layer will need to help hook up this software up to the data layer so that the game can be played." (Paragraph 4, Sentences 2 and 3)**
        
        - **These sentences detail that now we are moving on from our own AI players and are having the hackers
        connect their AI players ("hook up this software") to what is implied to be a server.**
      
      
    


- for the English of your memo, you may wish to check the following:

  - is each paragraph dedicated to a single topic? does it come with a
    thesis statement that specifies the topic?
    
    - **Yes. If we look at the system.pdf memo, we thought the memo was supposed to be constructed
    as a single essay, so it is just one paragraph. However, we have a clear thesis statement:
    "There are several components that will comprise the Fish game system as a whole..." (line 1)**
    
    - **We also mark our transition to the description of each component very clearly. 
    "First, let us consider the “presentation layer" (Line 4);
    "Next, we can consider the “data layer”" (Line 12);
    "Finally, we can consider the “logic layer”" (Lines 21-22);
    We could have potentially separated these into paragraphs.**
    
    - **In terms of the milestones.pdf, yes, we have every paragraph dedicated to a particular topic with
    clearly defined headers such as "Stage 1– Basic Rendering" and a general summary of what we want to accomplish. 
    For example, Paragraph 1, Line 1, "We will start simple: all we need for the first milestone is to render the UI, 
    with no functionality just yet" is a very clear thesis statement.**
    
  
   - do sentences make a point? do they run on?
   
     - **All sentences make a point and we do not have run on sentences. For example,
     "The logic component will be utilized in order to move from displaying the sign up page to Fish game board" from
     milestones.pdf, Paragraph 1, last sentence (lines 16-17). This sentence is very clear and concise and gets
     right to the point of what the logic component needs to do for this particular milestone.**
     
   
   - do sentences connect via old words/new words so that readers keep reading?
   
     - **Yes, in system.pdf, we made very clear transitions between component descriptions:
     "First, let us consider the “presentation layer" (Line 4);
     "Next, we can consider the “data layer”" (Line 12);
     "Finally, we can consider the “logic layer”" (Lines 21-22);**
    
     - **In terms of milestones.pdf, then yes, we have very clear headers for each paragraph such as 
     "Stage 1– Basic Rendering" and make sure to use certain sequential transitions when describing
     the sub steps of each stage. For example, "Then, the game board is rendered and the game will be played 
     manually by the 4 players." (Paragraph 2, Sentence 4) The use of 'Then' indicates the sequential aspect.**
    
   
   - are all sentences complete? Are they missing verbs? Objects? Other
     essential words?
     
     - **No, we do not have any sentences that are missing essential words. We use very clear and explicit
     sentences that have enough meaning. Here is a nice descriptive sentence we wrote:**
     
     - **"We also will add any finishing touches, especially making the presentation component more aesthetically pleasing, 
     and will address any outstanding bugs that have not already been fixed." (Milestones.pdf, Paragraph 5, Sentence 2)**
     
   
   - did you make sure that the spelling is correct? ("It's" is *not* a
    possesive; it's short for "it is". "There" is different from
    "their", a word that is too popular for your generation.)
    
     - **Yes, in both of our memos we made sure to spellcheck everything. We are not really sure what kind of an
     example to provide as everything is fine. Here is just an example sentence:**
     
     - **"We also will add any finishing touches, especially making the presentation component more aesthetically pleasing, 
     and will address any outstanding bugs that have not already been fixed." (Milestones.pdf, Paragraph 5, Sentence 2)**
     
     




The ideal feedback are pointers to specific senetences in your memo.
For PDF, the paragraph/sentence number suffices. 

For **code repos**, we will expect GitHub line-specific links. 


