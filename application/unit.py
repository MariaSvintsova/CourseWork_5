from __future__ import annotations
from abc import ABC, abstractmethod
from application.equipment import Equipment, Weapon, Armor
from application.classes import UnitClass
from random import randint
from typing import Optional


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name: str = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina: float = unit_class.max_stamina
        self.weapon: Weapon = Equipment().get_weapon(weapon_name='топорик')
        self.armor: Armor = Equipment().get_armor(armor_name='панцирь')
        self._is_skill_used: bool = False

    @property
    def health_points(self):
        return round(self.hp, 1)# TODO возвращаем аттрибут hp в красивом виде

    @property
    def stamina_points(self):
        return round(self.stamina, 1)# TODO возвращаем аттрибут hp в красивом виде

    def equip_weapon(self, weapon: Weapon):
        # TODO присваиваем нашему герою новое оружие
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        # TODO одеваем новую броню
        self.armor = armor
        return f"{self.name} экипирован броней {self.weapon.name}"

    def _count_damage(self, target: BaseUnit) -> float:
        # TODO Эта функция должна содержать:
        #  здесь же происходит уменьшение выносливости атакующего при ударе
        #  и уменьшение выносливости защищающегося при использовании брони
        #  если у защищающегося (target) нехватает выносливости - его броня игнорируется
        #  после всех расчетов цель получает урон - target.get_damage(damage)
        #  и возвращаем предполагаемый урон для последующего вывода пользователю в текстовом виде
        self.stamina -= self.weapon.stamina_per_hit * self.unit_class.stamina
        weapon_damage = self.weapon.damage * self.unit_class.attack

        if target.stamina > target.armor.stamina_per_turn * target.unit_class.stamina:
            target.stamina -= target.armor.stamina_per_turn * target.unit_class.stamina
            weapon_damage -= target.armor.defence * target.unit_class.attack

        return target.get_damage(damage=weapon_damage)

    def get_damage(self, damage: int) -> Optional[int]:
        # TODO получение урона целью
        #      присваиваем новое значение для аттрибута self.hp
        if self.hp > 0:
            self.hp -= damage
            return round(damage, 1)
        return None

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        метод использования умения.
        если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернем нам строку которая характеризует выполнение умения
        """
        if self._is_skill_used:
            return 'Навык использован'
        self._is_skill_used = True
        return self.unit_class.skill.use(user=self, target=target)


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """
        # TODO результат функции должен возвращать следующие строки:
        if self.stamina > self.weapon.stamina_per_hit * self.unit_class.stamina:
            damage = self._count_damage(target=target)
            if damage:
                return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."
            return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
        return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target)
        """
        # TODO результат функции должен возвращать результат функции skill.use или же следующие строки:
        if randint(1, 10) == 3 and self._is_skill_used:
            damage = self.use_skill(target)
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона."
        elif self.armor.defence > self.weapon.damage * self.unit_class.attack:
            return f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его останавливает."
        elif self.stamina < self.weapon.stamina_per_hit * self.unit_class.stamina:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        else:
            damage = self._count_damage(target)
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона."
