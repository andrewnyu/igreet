from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import KickoffForm
from app.models import User, Message
from app.main import bp
import random
import os

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')

def elo_ranking(a,b):
    '''
    Update the database given latest selection result, where player a was chosen over player b
    '''
    print(a.short_name)
    a.num_selections+=1
    b.num_selections+=1
    a.elo_ranking = int(((a.num_selections-1)*a.elo_ranking+(b.elo_ranking+400))/a.num_selections)
    b.elo_ranking = int(((b.num_selections-1)*b.elo_ranking+(a.elo_ranking-400))/b.num_selections)
    db.session.commit()

@bp.route('/choose/<player1>/<player2>')
def choose_player(player1, player2):
    player1 = Player.query.get(int(player1))
    player2 = Player.query.get(int(player2))

    selection = player1.player_id
    elo_ranking(player1, player2)

    result = Result(player1_id=player1.player_id, player2_id=player2.player_id, 
            selection=player1.player_id)
    db.session.add(result)
    db.session.commit()
    return redirect(url_for('main.kickoff'))


@bp.route('/kickoff', methods=['GET','POST'])
def kickoff():
    #generate players to compare using random numbers
    def get_players(player1=None,player2=None):
        player1 = random.randint(0,current_app.config['NUM_PLAYERS']-1) if player1 is None else player1
        player2 = random.randint(0,current_app.config['NUM_PLAYERS']-1) if player2 is None else player2
        while(player2 == player1):
            player2 = random.randint(0,current_app.config['NUM_PLAYERS']-1)
        return player1,player2

    player1,player2 = get_players()
    player1 = Player.query.get(int(player1))
    player2 = Player.query.get(int(player2))
    print(player1.short_name, player2.short_name)

    img1 = url_for('static',filename='img/'+str(player1.sofifa_id)+'.png')
    img2 = url_for('static',filename='img/'+str(player2.sofifa_id)+'.png')
        
    return render_template('main/kickoff.html', player1=player1, player2=player2, 
            img1 = img1, img2=img2)