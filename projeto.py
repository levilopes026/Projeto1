"""
🐉 Dragon's Quest - Jogo de aventura
Autor: Seu Nome
Descrição: Um jogo de aventura em texto com múltiplas escolhas, sistema de inventário e combate por turnos.
"""

import random
import time
import sys
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Item:
    name: str
    description: str
    value: int
    item_type: str  # 'weapon', 'potion', 'key'

@dataclass
class Enemy:
    name: str
    health: int
    damage: int
    description: str

class Player:
    def __init__(self, name: str):
        self.name = name
        self.health = 100
        self.max_health = 100
        self.inventory: List[Item] = []
        self.equipped_weapon = None
        self.gold = 50
        self.location = "village"
    
    def add_item(self, item: Item):
        self.inventory.append(item)
        print(f"🎒 {item.name} adicionado ao inventário!")
    
    def show_inventory(self):
        print(f"\n=== INVENTÁRIO DE {self.name.upper()} ===")
        print(f"❤️  Saúde: {self.health}/{self.max_health}")
        print(f"💰 Ouro: {self.gold}")
        print("Itens:")
        for i, item in enumerate(self.inventory, 1):
            print(f"  {i}. {item.name} - {item.description}")
    
    def use_potion(self):
        potions = [item for item in self.inventory if item.item_type == 'potion']
        if not potions:
            print("❌ Você não tem poções!")
            return False
        
        print("\n🍶 Escolha uma poção:")
        for i, potion in enumerate(potions, 1):
            print(f"{i}. {potion.name} (+{potion.value} HP)")
        
        try:
            choice = int(input("Sua escolha: ")) - 1
            if 0 <= choice < len(potions):
                potion = potions[choice]
                self.health = min(self.max_health, self.health + potion.value)
                self.inventory.remove(potion)
                print(f"🍶 Você usou {potion.name}! Saúde: {self.health}/{self.max_health}")
                return True
        except ValueError:
            pass
        return False

class Game:
    def __init__(self):
        self.player = None
        self.game_over = False
        self.locations = {
            "village": {
                "description": "🏠 Você está em uma vila pacífica. O povo precisa de ajuda!",
                "options": ["floresta", "loja", "taverna"]
            },
            "floresta": {
                "description": "🌲 Floresta densa com sons misteriosos...",
                "options": ["village", "caverna", "lago"]
            },
            "loja": {
                "description": "🏪 Loja do velho Merlin - itens mágicos à venda!",
                "options": ["village"]
            },
            "taverna": {
                "description": "🍻 A taverna 'Dragão Dourado'. Aventureiros compartilham histórias.",
                "options": ["village"]
            },
            "caverna": {
                "description": "🕳️ Caverna escura e úmida. Algo valioso pode estar aqui...",
                "options": ["floresta", "dragon_lair"]
            },
            "lago": {
                "description": "🏞️ Lago cristalino. Uma energia mágica emana das águas.",
                "options": ["floresta"]
            },
            "dragon_lair": {
                "description": "🐉 COVIL DO DRAGÃO! O dragão ancião guarda o tesouro!",
                "options": ["caverna"]
            }
        }
        
        self.items = {
            "espada": Item("Espada de Aço", "Uma espada confiável para batalhas", 15, "weapon"),
            "poção": Item("Poção de Cura", "Restaura 30 pontos de saúde", 30, "potion"),
            "chave": Item("Chave Antiga", "Abre portas trancadas", 0, "key"),
            "dragonslayer": Item("Espada Matadora de Dragões", "Lâmina lendária contra dragões", 40, "weapon")
        }
        
        self.enemies = {
            "goblin": Enemy("Goblin", 30, 10, "Uma criatura verde e perigosa"),
            "lobo": Enemy("Lobo Selvagem", 25, 15, "Feroz e rápido"),
            "dragão": Enemy("Dragão Ancião", 100, 25, "GUARDIÃO DO TESOURO FINAL")
        }

    def type_text(self, text: str, delay: float = 0.03):
        """Efeito de digitação"""
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def clear_screen(self):
        """Limpa a tela"""
        print("\n" * 50)

    def show_title(self):
        """Mostra título artístico"""
        title = """
        🐉╔═══════════════════════════════╗🐉
           │      DRAGON'S QUEST         │
           │    A Text Adventure Game    │
        🐉╚═══════════════════════════════╝🐉
        """
        print(title)

    def create_player(self):
        """Criação do personagem"""
        self.clear_screen()
        self.show_title()
        self.type_text("Bem-vindo, aventureiro!")
        name = input("\nQual é o seu nome? ").strip()
        self.player = Player(name)
        
        self.type_text(f"\n🌟 {name}, sua jornada épica começa agora!")
        self.type_text("O reino precisa de um herói para derrotar o Dragão Ancião!")
        input("\nPressione Enter para começar...")

    def combat(self, enemy_name: str):
        """Sistema de combate por turnos"""
        enemy = self.enemies[enemy_name]
        self.type_text(f"\n⚔️  ENCONTRO: {enemy.name} apareceu!")
        self.type_text(f"💀 {enemy.description}")
        
        while enemy.health > 0 and self.player.health > 0:
            print(f"\n❤️  Sua saúde: {self.player.health} | 💀 {enemy.name}: {enemy.health}")
            print("1. ⚔️  Atacar")
            print("2. 🍶 Usar poção")
            print("3. 🏃 Fugir")
            
            choice = input("Sua ação: ").strip()
            
            if choice == "1":
                # Player attack
                damage = random.randint(10, 20)
                if self.player.equipped_weapon:
                    damage += self.player.equipped_weapon.value
                
                enemy.health -= damage
                self.type_text(f"💥 Você ataca {enemy.name} causando {damage} de dano!")
                
                if enemy.health <= 0:
                    self.type_text(f"🎉 {enemy.name} foi derrotado!")
                    reward = random.randint(20, 50)
                    self.player.gold += reward
                    self.type_text(f"💰 Você ganhou {reward} de ouro!")
                    return True
            
            elif choice == "2":
                if not self.player.use_potion():
                    continue
            
            elif choice == "3":
                if random.random() < 0.5:  # 50% chance de fugir
                    self.type_text("🏃💨 Você fugiu da batalha!")
                    return False
                else:
                    self.type_text("❌ Falha ao fugir!")
            
            # Enemy attack
            if enemy.health > 0:
                enemy_damage = random.randint(5, enemy.damage)
                self.player.health -= enemy_damage
                self.type_text(f"🐉 {enemy.name} te ataca causando {enemy_damage} de dano!")
                
                if self.player.health <= 0:
                    self.type_text("💀 Você foi derrotado...")
                    self.game_over = True
                    return False
        
        return True

    def handle_location(self, location: str):
        """Lógica específica de cada localização"""
        self.clear_screen()
        current_loc = self.locations[location]
        
        self.type_text(f"\n📍 {current_loc['description']}")
        
        # Eventos especiais por localização
        if location == "village":
            self.type_text("\n👴 Um velho sábio te entrega uma espada!")
            self.player.add_item(self.items["espada"])
            self.player.equipped_weapon = self.items["espada"]
        
        elif location == "loja":
            self.type_text("\n🏪 Bem-vindo à loja do Merlin!")
            print("1. Comprar Poção de Cura - 30 ouros")
            print("2. Sair")
            
            if input("Sua escolha: ") == "1" and self.player.gold >= 30:
                self.player.gold -= 30
                self.player.add_item(self.items["poção"])
        
        elif location == "floresta":
            if random.random() < 0.6:  # 60% chance de encontro
                enemy = random.choice(["goblin", "lobo"])
                if not self.combat(enemy):
                    return
        
        elif location == "caverna":
            self.type_text("\n💎 Você encontrou uma chave antiga!")
            self.player.add_item(self.items["chave"])
        
        elif location == "lago":
            self.type_text("\n✨ As águas mágicas restauram sua saúde!")
            self.player.health = self.player.max_health
            print(f"❤️  Saúde restaurada: {self.player.health}")
        
        elif location == "dragon_lair":
            self.type_text("\n🔥 TESOURO ENCONTRADO! Mas o dragão guarda ferozmente!")
            if any(item.name == "Espada Matadora de Dragões" for item in self.player.inventory):
                self.type_text("⚔️  Você tem a Espada Lendária! Pode enfrentar o dragão!")
                if self.combat("dragão"):
                    self.victory()
            else:
                self.type_text("❌ Você precisa da Espada Matadora de Dragões!")
                self.type_text("💀 O dragão é muito forte! Fuja enquanto pode!")
                self.locations["dragon_lair"]["options"] = ["caverna"]

    def victory(self):
        """Final do jogo - vitória"""
        self.clear_screen()
        victory_text = """
        🎉╔═══════════════════════════════╗🎉
           │         VITÓRIA!            │
           │   O DRAGÃO FOI DERROTADO!   │
        🎉╚═══════════════════════════════╝🎉
        
        🌟 Parabéns, herói! O reino está salvo!
        💰 Tesouro adquirido: 1000 ouros
        🏆 Fama eterna garantida!
        """
        print(victory_text)
        self.game_over = True

    def play(self):
        """Loop principal do jogo"""
        self.create_player()
        
        while not self.game_over:
            self.clear_screen()
            
            # Mostrar status do jogador
            print(f"🧭 Localização: {self.player.location.upper()}")
            print(f"❤️  Saúde: {self.player.health} | 💰 Ouro: {self.player.gold}")
            
            # Mostrar opções de movimento
            current_loc = self.locations[self.player.location]
            print(f"\nPara onde você quer ir?")
            for i, option in enumerate(current_loc["options"], 1):
                print(f"{i}. {option.upper()}")
            print("I. 📦 Inventário")
            print("Q. 🚪 Sair do jogo")
            
            choice = input("\nSua escolha: ").lower().strip()
            
            if choice == "q":
                self.type_text("Até a próxima, aventureiro!")
                break
            elif choice == "i":
                self.player.show_inventory()
                input("\nPressione Enter para continuar...")
            elif choice.isdigit():
                choice_idx = int(choice) - 1
                if 0 <= choice_idx < len(current_loc["options"]):
                    new_location = current_loc["options"][choice_idx]
                    self.player.location = new_location
                    self.handle_location(new_location)
                    
                    if not self.game_over:
                        input("\nPressione Enter para continuar...")
                else:
                    self.type_text("❌ Escolha inválida!")
            else:
                self.type_text("❌ Comando não reconhecido!")

def main():
    """Função principal"""
    try:
        game = Game()
        game.play()
    except KeyboardInterrupt:
        print("\n\n👋 Jogo interrompido. Até logo!")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()