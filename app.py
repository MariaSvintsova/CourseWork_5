from flask import Flask, render_template, request, redirect, url_for
from unit import BaseUnit, PlayerUnit, EnemyUnit
from base import Arena
from classes import unit_classes
from equipment import Equipment

app = Flask(__name__)

heroes = {
    "player": BaseUnit,
    "enemy": BaseUnit
}

arena = Arena()


@app.route("/")
def menu_page():
    # TODO рендерим главное меню (шаблон index.html)
    return render_template('index.html')




@app.route("/fight/")
def start_fight():
    # TODO выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы
    # TODO рендерим экран боя (шаблон fight.html)
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])
    return render_template('fight.html', heroes=heroes, result='Attack!')

@app.route("/fight/hit")
def hit():
    # TODO кнопка нанесения удара
    # TODO обновляем экран боя (нанесение удара) (шаблон fight.html)
    # TODO если игра идет - вызываем метод player.hit() экземпляра класса арены
    if arena.game_is_running:
        return render_template('fight.html', heroes=heroes, result=arena.player_hit())
    else:
        return render_template('fight.html', heroes=heroes, result=arena.battle_result)
    # TODO если игра не идет - пропускаем срабатывание метода (простот рендерим шаблон с текущими данными)


@app.route("/fight/use-skill")
def use_skill():
    # TODO кнопка использования скилла
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    if arena.game_is_running:
        return render_template('fight.html', heroes=heroes, result=arena.player_use_skill())
    else:
        return render_template('fight.html', heroes=heroes, result=arena.battle_result)

@app.route("/fight/pass-turn")
def pass_turn():
    # TODO кнопка пропус хода
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    # TODO однако вызываем здесь функцию следующий ход (arena.next_turn())
    if arena.game_is_running:
        return render_template('fight.html', heroes=heroes, result=arena.next_turn())
    else:
        return render_template('fight.html', heroes=heroes, result=arena.battle_result)


@app.route("/fight/end-fight")
def end_fight():
    # TODO кнопка завершить игру - переход в главное меню
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    equipment = Equipment()

    if request.method == 'GET':
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        result = {
        "header": 'WAR GAME',      # для названия страниц
        "classes": unit_classes,    # для названия классов
        "weapons": weapons,    # для названия оружия
        "armors": armors       # для названия брони
    }
        return render_template('hero_choosing.html', result=result)

    elif request.method == 'POST':
        name = request.form['name']
        classes = request.form['unit_class']
        weapons = request.form['weapon']
        armors = request.form['armor']

        new_player = PlayerUnit(name=name, unit_class=unit_classes.get(classes))
        new_player.equip_weapon(equipment.get_weapon(weapons))
        new_player.equip_armor(equipment.get_armor(armors))

        heroes['player'] = new_player

        return redirect(url_for('choose_enemy'))




@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    equipment = Equipment()

    if request.method == 'GET':
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        result = {
        "header": 'WAR GAME',      # для названия страниц
        "classes": unit_classes,    # для названия классов
        "weapons": weapons,    # для названия оружия
        "armors": armors       # для названия брони
    }
        return render_template('hero_choosing.html', result=result)

    elif request.method == 'POST':
        name = request.form['name']
        classes = request.form['unit_class']
        weapons = request.form['weapon']
        armors = request.form['armor']
        print(classes)
        new_enemy = EnemyUnit(name=name, unit_class=unit_classes.get(classes))
        new_enemy.equip_weapon(equipment.get_weapon(weapons))
        new_enemy.equip_armor(equipment.get_armor(armors))

        heroes['enemy'] = new_enemy

        return redirect(url_for('start_fight'))


if __name__ == "__main__":
    app.run()
