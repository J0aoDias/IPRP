import time
import random
import functools
import turtle
turtle.addshape("maca.gif")
turtle.addshape('cara-cobra.gif')
MAX_X = 600
MAX_Y = 800
DEFAULT_SIZE = 20
SNAKE_SHAPE = 'cara-cobra.gif'

HIGH_SCORES_FILE_PATH = 'high_scores.txt'

SPEED = 0.08
parede = turtle.Turtle()
parede.speed(300)
parede.begin_fill()
parede.fillcolor('yellow')
parede.pensize(5)
parede.hideturtle()
parede.pu()
parede.goto(-300,-400)
parede.pd()
parede.goto(-300,400)
parede.goto(300,400)
parede.goto(300,-400)
parede.goto(-300,-400)
parede.end_fill()


def load_high_score(state):
    high_scores = open(HIGH_SCORES_FILE_PATH,'r')
    
    state['high_score'] = int(high_scores.readline())
    high_scores.close()
    # se já existir um high score devem guardar o valor em state['high_score']
    pass

def write_high_score_to_file(state):
    high_scores = open(HIGH_SCORES_FILE_PATH,'r')
    linhas= high_scores.readlines()
    high_scores.close()
    high_scores = open(HIGH_SCORES_FILE_PATH,'w')
    high_scores.write(str(state['high_score'])+'\n')
    high_scores.writelines(linhas)
    high_scores.close()
    
    # devem escrever o valor que está em state['high_score'] no ficheiro de high scores
    pass

def create_score_board(state):
    score_board = turtle.Turtle()
    score_board.speed(0)
    score_board.shape("square")
    score_board.color("black")
    score_board.penup()
    score_board.hideturtle()
    score_board.goto(0, MAX_Y / 2.2)
    state['score_board'] = score_board
    load_high_score(state)
    update_score_board(state)

def update_score_board(state):
    state['score_board'].clear()
    state['score_board'].write("Score: {} High Score: {}".format(state['score'], state['high_score']), align="center", font=("Helvetica", 24, "normal"))

def go_up(state):
    if state['snake']['current_direction'] != 'down':
        state['snake']['current_direction'] = 'up'

def go_down(state):
    if state['snake']['current_direction'] != 'up':
        state['snake']['current_direction'] = 'down'

def go_left(state):
    if state['snake']['current_direction'] != 'right':
        state['snake']['current_direction'] = 'left'

def go_right(state):
    if state['snake']['current_direction'] != 'left':
        state['snake']['current_direction'] = 'right'

def init_state():
    state = {}
    # Informação necessária para a criação do score board
    state['score_board'] = None
    state['new_high_score'] = False
    high_scores = open(HIGH_SCORES_FILE_PATH,'r')
    state['high_score'] = (high_scores.read())
    high_scores.close()
    state['score'] = 0
    # Para gerar a comida deverá criar um nova tartaruga e colocar a mesma numa posição aleatória do campo
    state['food'] = None
    state['window'] = None
    snake = {
        'head': None,                  # Variável que corresponde à cabeça da cobra
        'current_direction': None,  # Indicação da direcção atual do movimento da cobra
        'body' : []
    }
    state['snake'] = snake

    return state

def setup(state):
    window = turtle.Screen()
    window.setup(width=MAX_X, height=MAX_Y)
    window.listen()
    window.onkey(functools.partial(go_up, state), 'w')
    window.onkey(functools.partial(go_down, state), 's')
    window.onkey(functools.partial(go_left, state), 'a')
    window.onkey(functools.partial(go_right, state), 'd')
    window.tracer(0)
    state['window'] = window
    snake = state['snake']
    snake['current_direction'] = 'stop'
    snake['head'] = turtle.Turtle()
    snake['head'].shape(SNAKE_SHAPE)
    snake['head'].showturtle()
    snake['head'].pu()
    snake['head'].color('green')
    create_score_board(state)
    create_food(state)

def move(state):
    snake = state['snake']
    if snake['current_direction']!='stop':
        snake['head'].forward(20)
    
    if snake['current_direction'] == 'up':
        snake['head'].setheading(90)
   
    
    if snake['current_direction'] == 'down':
        snake['head'].setheading(-90)
    
    if snake['current_direction'] == 'right':
        snake['head'].setheading(0)
    
    if snake['current_direction'] == 'left':
        snake['head'].setheading(180)
    ''' 
    Função responsável pelo movimento da cobra no ambiente.
    '''
    snake = state['snake']

def create_food(state):
    snake = state['snake']
    snake_food = turtle.Turtle()
    snake_food.shape('maca.gif')
    snake_food.color("red")
    snake_food.penup()
    snake_food.goto(random.randint(-295,295),random.randint(-395,395))
    for i in range(len(snake['body'])):
        if snake_food.distance(snake['body']) < 15:
            snake_food.goto(random.randint(-295,295),random.randint(-395,395))
                               
                   
    state['food'] = snake_food
    ''' 
        Função responsável pela criação da comida. Note que elas deverão ser colocadas em posições aleatórias, mas dentro dos limites do ambiente.
    '''
    # a informação sobre a comida deve ser guardada em state['food']

def check_if_food_to_eat(state):
    
    snake = state['snake']
    snake_food = state['food']
    
    if snake['head'].distance(snake_food)< 15 :
        snake_food.goto(random.randint(-290,290),random.randint(-390,390))
        nova_tartaruga = turtle.Turtle()
        nova_tartaruga.speed(0)
        nova_tartaruga.shape('square')
        nova_tartaruga.color('black')
        nova_tartaruga.pu()
        snake['body'].append(nova_tartaruga)
        state['score'] = state['score'] + 10
        update_score_board(state)
        if state['score'] > state['high_score']:
            state['high_score'] = state['score']
            state['new_high_score'] = True
    update_score_board(state)
        
        
    ''' 
        Função responsável por verificar se a cobra tem uma peça de comida para comer. Deverá considerar que se a comida estiver a uma distância inferior a 15 pixels a cobra pode comer a peça de comida. 
    '''
   
    # para ler ou escrever os valores de high score, score e new high score, devem usar os respetivos campos do state: state['high_score'], state['score'] e state['new_high_score']

def boundaries_collision(state):
    snake = state['snake']
    
    if snake['head'].xcor() > 300 or snake['head'].xcor() < -300 or snake['head'].ycor() > 400 or snake['head'].ycor() < -400:
        lose= turtle.Turtle()
        lose.hideturtle()
        lose.goto(0,0)
        lose.write("   VOCE PERDEU! \nVOCE FOI CONTRA A PAREDE!\nA SUA PONTUAÇÃO FOI DE:{}".format(state['score']), align="center", font=("Helvetica", 24, "normal")) 
        
            
        
        
        
        return True
    else:
        return False
    
        
    ''' 
        Função responsável por verificar se a cobra colidiu com os limites do ambiente. Sempre que isto acontecer a função deverá returnar o valor booleano True, caso contrário retorna False.
    '''
    return False

def check_collisions(state):
    snake = state['snake']
  
    for a in snake['body']:
        if a.distance(snake['head']) <15 :
            lose = turtle.Turtle()
            lose.hideturtle()
           
            lose.goto(0,0)
            
            lose.write("   VOCE PERDEU! \n VOCÊ CHOCOU COM O SEU CORPO! \nA SUA PONTUAÇÃO FOI DE:{}".format(state['score']), align="center", font=("Helvetica", 24, "normal"))
            
            
            return True
        
    
    '''
        Função responsável por avaliar se há colisões. Atualmente apenas chama a função que verifica se há colisões com os limites do ambiente. No entanto deverá escrever o código para verificar quando é que a tartaruga choca com uma parede ou com o seu corpo.
    '''
    snake = state['snake']
    return boundaries_collision(state)
def seguir(state):
    snake = state['snake']
        
    for i in range(len(snake['body'])-1,0,-1):
        snake['body'][i].goto(snake['body'][i-1].xcor(),snake['body'][i-1].ycor())   
    
    if len(snake['body']) > 0 :
            snake['body'][0].goto(snake['head'].xcor(),snake['head'].ycor())   
def main():
    state = init_state()
    setup(state)
    while not check_collisions(state):
        state['window'].update()
        check_if_food_to_eat(state)
        seguir(state)
        move(state)
        time.sleep(SPEED) 
    print("YOU LOSE!")
    if state['new_high_score']:
        write_high_score_to_file(state)


main()