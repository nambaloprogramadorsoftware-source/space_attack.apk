import os
import random
import math

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.core.image import Image as CoreImage
from kivy.graphics import (
    Color,
    Ellipse,
    Rectangle,
    RoundedRectangle,
    Line,
    Triangle
)
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition


# =========================================================
# CONFIGURAÇÕES
# =========================================================

# Os recursos visuais e sonoros ficam junto do código e são incluídos no APK.
# O ficheiro do recorde fica na pasta privada da aplicação, onde pode ser escrito.
PASTA_RECURSOS = os.path.dirname(os.path.abspath(__file__))
PASTA = ""
JOGADOR_IMG = os.path.join(PASTA_RECURSOS, "jogador.png")
SOM_DISPARO = os.path.join(PASTA_RECURSOS, "disparo.mp3")
ARQUIVO_RECORDE = ""
CARTAZ_IMG = os.path.join(PASTA_RECURSOS, "cartaz.png")

Window.clearcolor = (
    0.01,
    0.02,
    0.10,
    1
)


# =========================================================
# CORES
# =========================================================

BRANCO = (1, 1, 1, 1)

AZUL = (
    0.05,
    0.30,
    0.80,
    1
)

ROXO = (
    0.45,
    0.12,
    0.75,
    1
)

VERDE = (
    0.05,
    0.70,
    0.25,
    1
)

VERMELHO = (
    0.80,
    0.08,
    0.08,
    1
)

VERMELHO_BOTAO = (
    0.90,
    0.05,
    0.05,
    1
)

AMARELO = (
    1,
    0.70,
    0.05,
    1
)

LARANJA_FOGO = (
    1,
    0.30,
    0.02,
    1
)

VERDE_ALIEN = (
    0.10,
    0.85,
    0.25,
    1
)

ROXO_ALIEN = (
    0.60,
    0.15,
    0.90,
    1
)

AZUL_ALIEN = (
    0.05,
    0.55,
    1.00,
    1
)


# =========================================================
# NÍVEIS DOS CHEFÕES
# =========================================================

NIVEIS_CHEFOES = {
    5,
    10,
    20,
    30,
    40,
    50,
    60
}


# =========================================================
# FUNDO ESPACIAL
# =========================================================

class FundoEspacial(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.estrelas = []
        self.velocidade = 2

        with self.canvas:

            Color(
                0.01,
                0.02,
                0.10,
                1
            )

            self.fundo = Rectangle(
                pos=self.pos,
                size=self.size
            )

            Color(
                1,
                1,
                1,
                0.8
            )

            for i in range(100):

                x = random.randint(
                    0,
                    max(
                        1,
                        int(Window.width)
                    )
                )

                y = random.randint(
                    0,
                    max(
                        1,
                        int(Window.height)
                    )
                )

                tamanho = random.choice(
                    [1, 1, 1, 2]
                )

                estrela = Ellipse(
                    pos=(x, y),
                    size=(tamanho, tamanho)
                )

                self.estrelas.append(
                    estrela
                )

        self.bind(
            pos=self.atualizar_fundo,
            size=self.atualizar_fundo
        )

        Clock.schedule_interval(
            self.animar_estrelas,
            1 / 60
        )

    def atualizar_fundo(self, *args):

        self.fundo.pos = self.pos
        self.fundo.size = self.size

    def animar_estrelas(self, dt):

        for estrela in self.estrelas:

            estrela.pos = (
                estrela.pos[0],
                estrela.pos[1] - self.velocidade
            )

            if estrela.pos[1] < 0:

                estrela.pos = (
                    random.randint(
                        0,
                        max(
                            1,
                            int(Window.width)
                        )
                    ),
                    Window.height + random.randint(
                        1,
                        30
                    )
                )


# =========================================================
# EXPLOSÃO
# =========================================================

class Explosao(Widget):

    def __init__(
        self,
        x,
        y,
        grande=False,
        **kwargs
    ):

        super().__init__(**kwargs)

        tamanho = 220 if grande else 60

        self.size = (
            tamanho,
            tamanho
        )

        self.pos = (
            x - tamanho / 2,
            y - tamanho / 2
        )

        self.tempo = 0
        self.particulas = []

        quantidade = 55 if grande else 8

        with self.canvas:

            if grande:

                Color(
                    1,
                    0.25,
                    0.02,
                    0.18
                )

                self.brilho = Ellipse(
                    pos=self.pos,
                    size=self.size
                )

            else:

                self.brilho = None

            for i in range(quantidade):

                Color(
                    1,
                    random.choice(
                        [
                            0.20,
                            0.40,
                            0.60,
                            0.80
                        ]
                    ),
                    0.05,
                    1
                )

                tamanho_particula = (
                    random.randint(6, 14)
                    if grande
                    else 7
                )

                particula = Ellipse(
                    pos=(x, y),
                    size=(
                        tamanho_particula,
                        tamanho_particula
                    )
                )

                self.particulas.append(
                    {
                        "obj": particula,
                        "dx": random.uniform(
                            -7 if grande else -2.5,
                            7 if grande else 2.5
                        ),
                        "dy": random.uniform(
                            -7 if grande else -2.5,
                            7 if grande else 2.5
                        )
                    }
                )

        Clock.schedule_interval(
            self.animar,
            1 / 60
        )

    def animar(self, dt):

        self.tempo += dt

        for particula in self.particulas:

            obj = particula["obj"]

            obj.pos = (
                obj.pos[0] + particula["dx"],
                obj.pos[1] + particula["dy"]
            )

            obj.size = (
                max(
                    1,
                    obj.size[0] - 0.35
                ),
                max(
                    1,
                    obj.size[1] - 0.35
                )
            )

        if self.tempo >= 0.55:

            Clock.unschedule(
                self.animar
            )

            if self.parent:

                self.parent.remove_widget(
                    self
                )


# =========================================================
# BOTÃO
# =========================================================

class BotaoJogo(Button):

    def __init__(
        self,
        cor=AZUL,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""

        self.background_color = (
            0,
            0,
            0,
            0
        )

        self.color = BRANCO
        self.bold = True

        with self.canvas.before:

            Color(
                cor[0],
                cor[1],
                cor[2],
                0.22
            )

            self.brilho = RoundedRectangle(
                pos=(
                    self.x - 4,
                    self.y - 4
                ),
                size=(
                    self.width + 8,
                    self.height + 8
                ),
                radius=[20]
            )

            Color(*cor)

            self.fundo = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[18]
            )

        self.bind(
            pos=self.atualizar,
            size=self.atualizar
        )

    def atualizar(self, *args):

        self.fundo.pos = self.pos
        self.fundo.size = self.size

        self.brilho.pos = (
            self.x - 4,
            self.y - 4
        )

        self.brilho.size = (
            self.width + 8,
            self.height + 8
        )


# =========================================================
# TIRO NORMAL
# =========================================================

class Tiro(Widget):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.size = (
            4,
            20
        )

        self.tempo = 0

        with self.canvas:

            Color(
                1,
                0.65,
                0.05,
                0.18
            )

            self.brilho = Ellipse(
                pos=(
                    self.x - 2,
                    self.y - 3
                ),
                size=(
                    10,
                    30
                )
            )

            Color(
                1,
                0.55,
                0.05,
                1
            )

            self.corpo = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[4]
            )

            Color(
                1,
                0.95,
                0.65,
                1
            )

            self.nucleo = RoundedRectangle(
                pos=(
                    self.x + 2,
                    self.y + 5
                ),
                size=(
                    4,
                    18
                ),
                radius=[2]
            )

        self.bind(
            pos=self.atualizar
        )

    def atualizar(self, *args):

        self.corpo.pos = self.pos

        self.nucleo.pos = (
            self.x + 2,
            self.y + 5
        )

        self.brilho.pos = (
            self.x - 2,
            self.y - 3
        )

    def animar(self, dt):

        self.tempo += dt


# =========================================================
# BOMBA
# =========================================================

class Bomba(Widget):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.size = (
            24,
            42
        )

        self.tempo = 0

        with self.canvas:

            Color(
                1,
                0.30,
                0.02,
                0.18
            )

            self.brilho = Ellipse(
                pos=(
                    self.x - 5,
                    self.y - 5
                ),
                size=(
                    34,
                    52
                )
            )

            Color(
                0.08,
                0.08,
                0.10,
                1
            )

            self.corpo = Ellipse(
                pos=self.pos,
                size=self.size
            )

            Color(
                0.90,
                0.05,
                0.03,
                1
            )

            self.faixa = Rectangle(
                pos=(
                    self.x,
                    self.y + 14
                ),
                size=(
                    self.width,
                    6
                )
            )

            Color(
                0.35,
                0.35,
                0.40,
                1
            )

            self.ponta = Ellipse(
                pos=(
                    self.x + 6,
                    self.y + self.height - 7
                ),
                size=(
                    12,
                    12
                )
            )

            Color(
                1,
                0.15,
                0.02,
                1
            )

            self.luz = Ellipse(
                size=(
                    6,
                    6
                )
            )

        self.bind(
            pos=self.atualizar
        )

    def atualizar(self, *args):

        self.corpo.pos = self.pos
        self.corpo.size = self.size

        self.brilho.pos = (
            self.x - 1,
            self.y - 1
        )

        self.faixa.pos = (
            self.x,
            self.y + 10
        )

        self.faixa.size = (
            self.width,
            6
        )

        self.ponta.pos = (
            self.x + 6,
            self.y + self.height - 7
        )

        self.luz.pos = (
            self.x + 9,
            self.y + 22
        )

    def animar(self, dt):

        self.tempo += dt

        pulsacao = (
            math.sin(
                self.tempo * 10
            ) + 1
        ) / 2

        tamanho = (
            30 + pulsacao * 4
        )

        self.brilho.size = (
            tamanho,
            tamanho + 5
        )

        self.brilho.pos = (
            self.center_x - tamanho / 1,
            self.center_y - tamanho / 1
        )


# =========================================================
# ALIEN
# =========================================================

class Alien(Widget):

    def __init__(
        self,
        velocidade=3,
        cor=None,
        tamanho=70,
        fala="",
        **kwargs
    ):

        super().__init__(**kwargs)

        self.size = (
            tamanho,
            tamanho
        )

        self.velocidade = velocidade

        self.vida = 1
        self.vida_maxima = 1

        self.tempo_boca = random.uniform(
            0,
            math.tau
        )

        self.velocidade_boca = random.uniform(
            7.0,
            10.0
        )

        if cor is None:

            self.cor_alien = random.choice(
                [
                    VERDE_ALIEN,
                    ROXO_ALIEN,
                    AZUL_ALIEN
                ]
            )

        else:

            self.cor_alien = cor

        with self.canvas:

            Color(*self.cor_alien)

            self.antena_esq = Line(
                width=2
            )

            self.antena_dir = Line(
                width=2
            )

            Color(
                1,
                0.2,
                0.2,
                1
            )

            self.ponta_esq = Ellipse(
                size=(7, 7)
            )

            self.ponta_dir = Ellipse(
                size=(7, 7)
            )

            Color(*self.cor_alien)

            self.cabeca = RoundedRectangle(
                radius=[20]
            )

            Color(
                0.8,
                0.02,
                0.02,
                1
            )

            self.olho_esq = Ellipse(
                size=(13, 17)
            )

            self.olho_dir = Ellipse(
                size=(13, 17)
            )

            Color(
                1,
                0.6,
                0.6,
                1
            )

            self.brilho_esq = Ellipse(
                size=(4, 5)
            )

            self.brilho_dir = Ellipse(
                size=(4, 5)
            )

            Color(
                0.01,
                0.01,
                0.01,
                1
            )

            self.boca = RoundedRectangle(
                radius=[10]
            )

            Color(
                1,
                1,
                1,
                1
            )

            self.dentes = []

            for i in range(8):

                dente = Rectangle(
                    size=(7, 9)
                )

                self.dentes.append(
                    dente
                )

        self.fala_label = Label(
            text=fala,
            color=BRANCO,
            bold=True,
            font_size=11,
            size_hint=(None, None),
            size=(180, 32),
            halign="center",
            valign="middle"
        )

        self.add_widget(
            self.fala_label
        )

        self.bind(
            pos=self.atualizar_desenho,
            size=self.atualizar_desenho
        )

        self.atualizar_desenho()

    def atualizar_desenho(self, *args):

        x = self.x
        y = self.y
        w = self.width
        h = self.height

        self.antena_esq.points = [
            x + w * 0.25,
            y + h * 0.72,
            x + w * 0.10,
            y + h * 0.95
        ]

        self.antena_dir.points = [
            x + w * 0.75,
            y + h * 0.72,
            x + w * 0.90,
            y + h * 0.95
        ]

        self.ponta_esq.pos = (
            x + w * 0.05,
            y + h * 0.92
        )

        self.ponta_dir.pos = (
            x + w * 0.85,
            y + h * 0.92
        )

        self.cabeca.pos = (
            x,
            y + h * 0.15
        )

        self.cabeca.size = (
            w,
            h * 0.65
        )

        self.olho_esq.pos = (
            x + w * 0.20,
            y + h * 0.50
        )

        self.olho_dir.pos = (
            x + w * 0.61,
            y + h * 0.50
        )

        self.brilho_esq.pos = (
            x + w * 0.23,
            y + h * 0.59
        )

        self.brilho_dir.pos = (
            x + w * 0.64,
            y + h * 0.59
        )

        self.fala_label.pos = (
            x + w / 2 - 90,
            y + h + 3
        )

        self.atualizar_boca()

    def atualizar_boca(self):

        x = self.x
        y = self.y
        w = self.width
        h = self.height

        abertura = (
            math.sin(self.tempo_boca) + 1
        ) / 2

        abertura = abertura ** 1.5

        altura_boca = h * (
            0.13
            + 0.28 * abertura
        )

        centro_boca = y + h * 0.34

        boca_y = (
            centro_boca
            - altura_boca / 2
        )

        self.boca.pos = (
            x + w * 0.18,
            boca_y
        )

        self.boca.size = (
            w * 0.64,
            altura_boca
        )

        for i, dente in enumerate(
            self.dentes
        ):

            coluna = i % 4

            dente.size = (
                w * 0.08,
                h * 0.09
            )

            pos_x = (
                x
                + w * 0.23
                + coluna * w * 0.15
            )

            if i < 4:

                pos_y = (
                    boca_y
                    + altura_boca * 0.58
                )

            else:

                pos_y = (
                    boca_y
                    + altura_boca * 0.07
                )

            dente.pos = (
                pos_x,
                pos_y
            )

    def animar_boca(self, dt):

        self.tempo_boca += (
            dt * self.velocidade_boca
        )

        self.atualizar_boca()


# =========================================================
# NAVE DO CHEFÃO
# =========================================================

class NaveChefao(Widget):

    def __init__(
        self,
        nivel,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.nivel = nivel

        if nivel == 60:
            tamanho = 300
        elif nivel >= 50:
            tamanho = 280
        elif nivel >= 40:
            tamanho = 260
        elif nivel >= 30:
            tamanho = 245
        elif nivel >= 20:
            tamanho = 230
        elif nivel >= 10:
            tamanho = 215
        else:
            tamanho = 200

        self.size = (
            tamanho,
            tamanho * 0.38
        )

        self.criar_desenho()

        self.bind(
            pos=self.atualizar
        )

        self.atualizar()

    def criar_desenho(self):

        with self.canvas:

            Color(
                0.12,
                0.12,
                0.18,
                1
            )

            self.corpo = RoundedRectangle(
                radius=[25]
            )

            Color(
                0.30,
                0.02,
                0.35,
                1
            )

            self.parte_cima = Ellipse()

            Color(
                1,
                0.05,
                0.05,
                1
            )

            self.luz_esq = Ellipse(
                size=(15, 15)
            )

            self.luz_meio = Ellipse(
                size=(18, 18)
            )

            self.luz_dir = Ellipse(
                size=(15, 15)
            )

            Color(
                0.07,
                0.08,
                0.14,
                1
            )

            self.asa_esq = Triangle()
            self.asa_dir = Triangle()

            Color(
                0.55,
                0.05,
                0.08,
                1
            )

            self.canhao_esq = RoundedRectangle(
                radius=[5]
            )

            self.canhao_dir = RoundedRectangle(
                radius=[5]
            )

            Color(
                1,
                0.65,
                0.05,
                1
            )

            self.luz_central = Ellipse(
                size=(22, 22)
            )

    def atualizar(self, *args):

        x = self.x
        y = self.y
        w = self.width
        h = self.height

        self.corpo.pos = (
            x,
            y
        )

        self.corpo.size = (
            w,
            h
        )

        self.parte_cima.pos = (
            x + w * 0.30,
            y + h * 0.25
        )

        self.parte_cima.size = (
            w * 0.40,
            h * 0.75
        )

        self.luz_esq.pos = (
            x + w * 0.25,
            y + h * 0.30
        )

        self.luz_meio.pos = (
            x + w * 0.47,
            y + h * 0.38
        )

        self.luz_dir.pos = (
            x + w * 0.70,
            y + h * 0.30
        )

        self.asa_esq.points = [
            x,
            y + h * 0.25,
            x - w * 0.25,
            y - h * 0.15,
            x + w * 0.18,
            y + h * 0.45
        ]

        self.asa_dir.points = [
            x + w,
            y + h * 0.25,
            x + w * 1.25,
            y - h * 0.15,
            x + w * 0.82,
            y + h * 0.45
        ]

        self.canhao_esq.pos = (
            x + w * 0.18,
            y - h * 0.05
        )

        self.canhao_esq.size = (
            w * 0.10,
            h * 0.35
        )

        self.canhao_dir.pos = (
            x + w * 0.72,
            y - h * 0.05
        )

        self.canhao_dir.size = (
            w * 0.10,
            h * 0.35
        )

        self.luz_central.pos = (
            x + w * 0.46,
            y + h * 0.05
        )


# =========================================================
# CHEFÃO
# =========================================================

class Chefao(Widget):

    def __init__(
        self,
        nivel,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.nivel = nivel

        tamanhos = {
            5: 156,
            10: 200,
            20: 250,
            30: 260,
            40: 270,
            50: 280,
            60: 300
        }

        tamanho = tamanhos.get(
            nivel,
            150
        )

        self.size = (
            tamanho,
            tamanho
        )

        self.velocidade = {
            5: 1.5,
            10: 1.6,
            20: 1.7,
            30: 1.8,
            40: 1.9,
            50: 2.0,
            60: 2.1
        }.get(
            nivel,
            1.5
        )

        self.direcao = 1

        self.vida_maxima = {
            5: 300,
            10: 400,
            20: 700,
            30: 800,
            40: 900,
            50: 1000,
            60: 10000
        }.get(
            nivel,
            150
        )

        self.vida = self.vida_maxima

        self.tempo_boca = random.uniform(
            0,
            math.tau
        )

        self.velocidade_boca = random.uniform(
            4.0,
            5.5
        )

        self.tempo_entrada = 0
        self.tempo_parado = 5
        self.saiu_da_nave = False

        self.nomes = {
            5: "SOMBRA VERDE",
            10: "DEVORADOR ROXO",
            20: "TITÃ AZUL",
            30: "DEMÓNIO CÓSMICO",
            40: "GUARDIÃO NEGRO",
            50: "FUSTRADO",
            60: "O  CHEFÃO"
        }

        self.nome_chefao = self.nomes.get(
            nivel,
            "CHEFÃO"
        )

        self.falas = {
            5: "Ebenesis... encontraste-me!",
            10: "O espaço pertence-nos!",
            20: "Não vais passar daqui!",
            30: "A tua missão termina aqui!",
            40: "Eu sou o guardião do vazio!",
            50: "Ninguém escapa do meu domínio!",
            60: "O desafio final começou!"
        }

        self.fala = self.falas.get(
            nivel,
            "Cheguei!"
        )

        self.criar_desenho()

        self.nome = Label(
            text=(
                "👹 "
                + self.nome_chefao
                + " 👹"
            ),
            color=AMARELO,
            bold=True,
            font_size=14,
            size_hint=(None, None),
            size=(300, 35),
            halign="center"
        )

        self.fala_label = Label(
            text=self.fala,
            color=BRANCO,
            bold=True,
            font_size=12,
            size_hint=(None, None),
            size=(320, 40),
            halign="center",
            valign="middle"
        )

        self.contagem = Label(
            text="5",
            color=VERMELHO,
            bold=True,
            font_size=28,
            size_hint=(None, None),
            size=(100, 50),
            halign="center"
        )

        self.add_widget(self.nome)
        self.add_widget(self.fala_label)
        self.add_widget(self.contagem)

        self.bind(
            pos=self.atualizar,
            size=self.atualizar
        )

        self.atualizar()

    def criar_desenho(self):

        with self.canvas:

            cores = {
                5: (0.05, 0.45, 0.12, 1),
                10: (0.35, 0.02, 0.65, 1),
                20: (0.02, 0.30, 0.75, 1),
                30: (0.70, 0.05, 0.02, 1),
                40: (0.04, 0.04, 0.06, 1),
                50: (0.28, 0.01, 0.40, 1),
                60: (0.18, 0.01, 0.01, 1)
            }

            cor = cores.get(
                self.nivel,
                (0.3, 0.1, 0.3, 1)
            )

            Color(*cor)

            self.corpo = RoundedRectangle(
                radius=[35]
            )

            Color(
                0.10,
                0.10,
                0.15,
                1
            )

            self.armadura = RoundedRectangle(
                radius=[30]
            )

            Color(
                1,
                0.02,
                0.02,
                1
            )

            self.olho_esq = Ellipse(
                size=(28, 35)
            )

            self.olho_dir = Ellipse(
                size=(28, 35)
            )

            if self.nivel >= 10:

                Color(
                    1,
                    0.60,
                    0.02,
                    1
                )

                self.olho_central = Ellipse(
                    size=(24, 30)
                )

            else:

                self.olho_central = None

            Color(
                1,
                0.85,
                0.20,
                1
            )

            self.luz_esq = Ellipse(
                size=(8, 9)
            )

            self.luz_dir = Ellipse(
                size=(8, 9)
            )

            Color(
                0.01,
                0.01,
                0.01,
                1
            )

            self.boca = RoundedRectangle(
                radius=[15]
            )

            Color(
                1,
                1,
                0.75,
                1
            )

            self.dentes = []

            for i in range(12):

                dente = Rectangle(
                    size=(9, 15)
                )

                self.dentes.append(dente)

            Color(
                0.95,
                0.05,
                0.03,
                1
            )

            self.espinho_esq = Line(
                width=6
            )

            self.espinho_dir = Line(
                width=6
            )

            self.espinho_cima = Line(
                width=6
            )

            Color(
                1,
                0.15,
                0.02,
                0.95
            )

            self.nucleo = Ellipse(
                size=(32, 32)
            )

            Color(
                0.03,
                0.03,
                0.03,
                1
            )

            self.barra_fundo = RoundedRectangle(
                radius=[8]
            )

            Color(
                1,
                0.03,
                0.03,
                1
            )

            self.barra_vida = RoundedRectangle(
                radius=[8]
            )

    def atualizar(self, *args):

        x = self.x
        y = self.y
        w = self.width
        h = self.height

        self.corpo.pos = (x, y)
        self.corpo.size = (w, h)

        self.armadura.pos = (
            x + w * 0.08,
            y + h * 0.08
        )

        self.armadura.size = (
            w * 0.84,
            h * 0.84
        )

        self.olho_esq.pos = (
            x + w * 0.16,
            y + h * 0.52
        )

        self.olho_dir.pos = (
            x + w * 0.66,
            y + h * 0.52
        )

        if self.olho_central:

            self.olho_central.pos = (
                x + w * 0.42,
                y + h * 0.68
            )

        self.luz_esq.pos = (
            x + w * 0.22,
            y + h * 0.68
        )

        self.luz_dir.pos = (
            x + w * 0.72,
            y + h * 0.68
        )

        self.espinho_esq.points = [
            x,
            y + h * 0.45,
            x - w * 0.20,
            y + h * 0.72,
            x,
            y + h * 0.90
        ]

        self.espinho_dir.points = [
            x + w,
            y + h * 0.45,
            x + w * 1.20,
            y + h * 0.72,
            x + w,
            y + h * 0.90
        ]

        self.espinho_cima.points = [
            x + w * 0.25,
            y + h * 0.90,
            x + w * 0.50,
            y + h * 1.15,
            x + w * 0.75,
            y + h * 0.90
        ]

        self.nucleo.pos = (
            x + w * 0.43,
            y + h * 0.38
        )

        self.barra_fundo.pos = (
            x,
            y + h + 48
        )

        self.barra_fundo.size = (
            w,
            13
        )

        proporcao = max(
            0,
            self.vida / self.vida_maxima
        )

        self.barra_vida.pos = (
            x,
            y + h + 48
        )

        self.barra_vida.size = (
            w * proporcao,
            13
        )

        self.nome.pos = (
            x + w / 2 - 150,
            y + h + 17
        )

        self.fala_label.pos = (
            x + w / 2 - 160,
            y - 48
        )

        self.contagem.pos = (
            x + w / 2 - 50,
            y + h / 2 - 25
        )

        self.atualizar_boca()

    def atualizar_boca(self):

        x = self.x
        y = self.y
        w = self.width
        h = self.height

        abertura = (
            math.sin(self.tempo_boca) + 1
        ) / 2

        abertura = abertura ** 1.35

        altura_boca = h * (
            0.14
            + 0.30 * abertura
        )

        centro_boca = y + h * 0.33

        boca_y = (
            centro_boca
            - altura_boca / 2
        )

        self.boca.pos = (
            x + w * 0.20,
            boca_y
        )

        self.boca.size = (
            w * 0.60,
            altura_boca
        )

        for i, dente in enumerate(
            self.dentes
        ):

            coluna = i % 6

            dente.size = (
                w * 0.07,
                h * 0.08
            )

            pos_x = (
                x
                + w * 0.25
                + coluna * w * 0.09
            )

            if i < 6:

                pos_y = (
                    boca_y
                    + altura_boca * 0.60
                )

            else:

                pos_y = (
                    boca_y
                    + altura_boca * 0.05
                )

            dente.pos = (
                pos_x,
                pos_y
            )

    def animar_boca(self, dt):

        self.tempo_boca += (
            dt * self.velocidade_boca
        )

        self.atualizar_boca()

    def receber_dano(self, dano):

        self.vida -= dano

        if self.vida < 0:
            self.vida = 0


# =========================================================
# NAVE DO JOGO
# =========================================================

class Jogo(FloatLayout):

    def __init__(
        self,
        novo_jogo_callback=None,
        menu_callback=None,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.novo_jogo_callback = novo_jogo_callback
        self.menu_callback = menu_callback

        self.pontos = 0
        self.vidas = 5
        self.nivel = 1

        self.inimigos = []
        self.tiros = []
        self.bombas = []

        self.chefao = None
        self.nave_chefao = None

        self.chefao_niveis_derrotados = set()

        self.pausado = False
        self.jogo_terminou = False
        self.jogo_concluido = False
        self.inicio_pronto = False

        self.tempo_recarga_fogo = 0
        self.recarga_fogo_maxima = 5

        self.som_disparo = None

        if os.path.exists(SOM_DISPARO):

            self.som_disparo = SoundLoader.load(
                SOM_DISPARO
            )

            if self.som_disparo:
                self.som_disparo.volume = 0.7

        self.fundo = FundoEspacial()

        self.add_widget(self.fundo)

        self.aliens_layer = Widget()
        self.nave_chefao_layer = Widget()
        self.chefao_layer = Widget()
        self.tiros_layer = Widget()
        self.explosoes_layer = Widget()

        self.add_widget(self.aliens_layer)
        self.add_widget(self.nave_chefao_layer)
        self.add_widget(self.chefao_layer)
        self.add_widget(self.tiros_layer)
        self.add_widget(self.explosoes_layer)

        if os.path.exists(JOGADOR_IMG):

            self.jogador = Image(
                source=JOGADOR_IMG,
                size_hint=(
                    None,
                    None
                ),
                size=(
                    180,
                    120
                ),
                allow_stretch=True,
                keep_ratio=True
            )

        else:

            self.jogador = Widget(
                size_hint=(
                    None,
                    None
                ),
                size=(
                    180,
                    120
                )
            )

            with self.jogador.canvas:

                Color(*AZUL)

                self.jogador.corpo = RoundedRectangle(
                    pos=self.jogador.pos,
                    size=self.jogador.size
                )

            self.jogador.bind(
                pos=self.atualizar_jogador_fallback,
                size=self.atualizar_jogador_fallback
            )

        self.jogador.pos = (
            Window.width / 2 - self.jogador.width / 2,
            125
        )

        self.add_widget(
            self.jogador
        )

        self.criar_hud()
        self.criar_botoes()

        self.mensagem_inicio = Label(
            text=(
                "Ebenesis, chegou a hora "
                "de salvar o mundo!"
            ),
            color=BRANCO,
            bold=True,
            font_size=20,
            halign="center",
            valign="middle",
            size_hint=(
                0.90,
                None
            ),
            height=80,
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.55
            }
        )

        self.mensagem_inicio.bind(
            size=lambda obj, value:
            setattr(
                obj,
                "text_size",
                value
            )
        )

        self.add_widget(
            self.mensagem_inicio
        )

        Clock.schedule_interval(
            self.atualizar,
            1 / 60
        )

        Clock.schedule_interval(
            self.criar_inimigo,
            0.80
        )

        Clock.schedule_interval(
            self.atirar_automaticamente,
            0.35
        )

        Clock.schedule_once(
            self.iniciar_jogo,
            0.1
        )

        Clock.schedule_once(
            self.remover_mensagem_inicio,
            2
        )

    def iniciar_jogo(self, dt):

        if self.jogo_terminou:
            return

        self.inicio_pronto = True

        self.criar_primeiros_aliens(0)

        self.atirar_automaticamente(0)

    def remover_mensagem_inicio(self, dt):

        if self.mensagem_inicio.parent:
            self.remove_widget(
                self.mensagem_inicio
            )

    def atualizar_jogador_fallback(self, *args):

        self.jogador.corpo.pos = (
            self.jogador.pos
        )

        self.jogador.corpo.size = (
            self.jogador.size
        )

    def criar_hud(self):

        self.hud = BoxLayout(
            orientation="horizontal",
            size_hint=(
                1,
                None
            ),
            height=55,
            pos_hint={
                "top": 1
            },
            padding=[
                8,
                5
            ],
            spacing=8
        )

        if os.path.exists(JOGADOR_IMG):

            mini = Image(
                source=JOGADOR_IMG,
                size_hint=(
                    None,
                    None
                ),
                size=(
                    30,
                    30
                ),
                allow_stretch=True,
                keep_ratio=True
            )

            self.hud.add_widget(mini)

        self.label_pontos = Label(
            text="Pontos: 0",
            color=BRANCO,
            bold=True
        )

        self.label_nivel = Label(
            text="Nivel: 1",
            color=BRANCO,
            bold=True
        )

        self.label_recorde = Label(
            text=(
                "Recorde: "
                + str(self.ler_recorde())
            ),
            color=BRANCO,
            bold=True
        )

        self.label_vidas = Label(
            text="vida:5",
            color=BRANCO,
            bold=True,
            font_size=19
        )

        self.hud.add_widget(self.label_pontos)
        self.hud.add_widget(self.label_nivel)
        self.hud.add_widget(self.label_recorde)
        self.hud.add_widget(self.label_vidas)

        self.add_widget(self.hud)

    def criar_botoes(self):

        self.botoes_layout = BoxLayout(
            orientation="horizontal",
            size_hint=(
                0.94,
                None
            ),
            height=62,
            spacing=8,
            pos_hint={
                "center_x": 0.5,
                "y": 0.02
            }
        )

        self.botao_esquerda = BotaoJogo(
            text="ESQ.",
            cor=AZUL,
            font_size=30
        )

        self.botao_fogo = BotaoJogo(
            text="EXPLOSIVO",
            cor=LARANJA_FOGO,
            font_size=15
        )

        self.botao_pausar = BotaoJogo(
            text="PAUSAR",
            cor=VERMELHO_BOTAO,
            font_size=15
        )

        self.botao_direita = BotaoJogo(
            text="DIR.",
            cor=ROXO,
            font_size=30
        )

        self.botao_esquerda.bind(
            on_press=self.mover_esquerda
        )

        self.botao_fogo.bind(
            on_press=self.disparo_manual
        )

        self.botao_pausar.bind(
            on_press=self.pausar
        )

        self.botao_direita.bind(
            on_press=self.mover_direita
        )

        self.botoes_layout.add_widget(
            self.botao_esquerda
        )

        self.botoes_layout.add_widget(
            self.botao_fogo
        )

        self.botoes_layout.add_widget(
            self.botao_pausar
        )

        self.botoes_layout.add_widget(
            self.botao_direita
        )

        self.add_widget(
            self.botoes_layout
        )

    # =====================================================
    # MOVIMENTO DA NAVE — AJUSTADO PARA A IMAGEM
    # =====================================================

    def mover_esquerda(self, *args):

        if not self.inicio_pronto:
            return

        if self.pausado:
            return

        if self.jogo_terminou:
            return

        # Margem transparente estimada do jogador.png
        margem_esquerda = self.jogador.width * 0.30

        self.jogador.x -= 45

        # Permite que o Widget passe ligeiramente
        # para fora do ecrã.
        limite_esquerdo = -margem_esquerda

        if self.jogador.x < limite_esquerdo:
            self.jogador.x = limite_esquerdo

    def mover_direita(self, *args):

        if not self.inicio_pronto:
            return

        if self.pausado:
            return

        if self.jogo_terminou:
            return

        # Margem transparente estimada do jogador.png
        margem_direita = self.jogador.width * 0.20

        self.jogador.x += 45

        # Permite que o Widget passe ligeiramente
        # para fora do ecrã.
        limite_direito = (
            self.width
            - self.jogador.width
            + margem_direita
        )

        if self.jogador.x > limite_direito:
            self.jogador.x = limite_direito

    def pausar(self, *args):

        if not self.inicio_pronto:
            return

        if self.jogo_terminou:
            return

        self.pausado = not self.pausado

        if self.pausado:
            self.botao_pausar.text = "▶"
        else:
            self.botao_pausar.text = "PAUSAR"

    # =====================================================
    # TIRO AUTOMÁTICO
    # =====================================================

    def criar_tiro(self):

        tiro = Tiro()

        tiro.x = (
            self.jogador.x
            + self.jogador.width * 0.28
            + 50
            - tiro.width / 2
        )

        tiro.y = (
            self.jogador.y
            + self.jogador.height * 0.90
        )

        self.tiros.append(tiro)

        self.tiros_layer.add_widget(
            tiro
        )

        if self.som_disparo:

            self.som_disparo.stop()
            self.som_disparo.play()

    def criar_bomba(self):

        bomba = Bomba()

        bomba.x = (
            self.jogador.x
            + self.jogador.width * 0.10
            + 50
            - bomba.width / 2
        )

        bomba.y = (
            self.jogador.y
            + self.jogador.height * 0.72
        )

        self.bombas.append(bomba)

        self.tiros_layer.add_widget(
            bomba
        )

        if self.som_disparo:

            self.som_disparo.stop()
            self.som_disparo.play()

    def disparo_manual(self, *args):

        if not self.inicio_pronto:
            return

        if self.pausado:
            return

        if self.jogo_terminou:
            return

        if self.tempo_recarga_fogo > 0:
            return

        self.criar_bomba()

        self.tempo_recarga_fogo = (
            self.recarga_fogo_maxima
        )

        self.atualizar_botao_fogo()

    def atualizar_botao_fogo(self):

        if self.tempo_recarga_fogo > 0:

            segundos = int(
                math.ceil(
                    self.tempo_recarga_fogo
                )
            )

            self.botao_fogo.text = (
                "💣 "
                + str(segundos)
                + "s"
            )

        else:

            self.botao_fogo.text = "FOGO"

    def atirar_automaticamente(self, dt):

        if not self.inicio_pronto:
            return

        if self.pausado:
            return

        if self.jogo_terminou:
            return

        self.criar_tiro()

    def tamanho_alien_atual(self):

        return min(
            130,
            70 + (self.nivel - 1) * 3
        )

    def velocidade_alien_atual(self):

        return min(
            16,
            5 + (self.nivel - 1) * 0.20
        )

    def vida_alien_atual(self):

        return min(
            15,
            1 + (self.nivel - 1) // 5
        )

    def criar_primeiros_aliens(self, dt):

        if self.jogo_terminou:
            return

        cores = [
            VERDE_ALIEN,
            ROXO_ALIEN,
            AZUL_ALIEN
        ]

        tamanho = self.tamanho_alien_atual()
        velocidade = self.velocidade_alien_atual()
        vida_alien = self.vida_alien_atual()

        for i in range(3):

            alien = Alien(
                velocidade=velocidade,
                cor=cores[i],
                tamanho=tamanho
            )

            alien.vida = vida_alien
            alien.vida_maxima = vida_alien

            alien.x = (
                40 + i * 120
            )

            alien.y = (
                Window.height
                - tamanho
                - 60
                - i * 90
            )

            self.inimigos.append(alien)

            self.aliens_layer.add_widget(
                alien
            )

    def criar_inimigo(self, dt):

        if not self.inicio_pronto:
            return

        if self.pausado:
            return

        if self.jogo_terminou:
            return

        if self.chefao:
            return

        if self.nave_chefao:
            return

        velocidade = self.velocidade_alien_atual()
        tamanho = self.tamanho_alien_atual()
        vida_alien = self.vida_alien_atual()

        fala = ""

        if self.nivel >= 5:

            falas = [
                "Hoje vais ser apanhado! 😂",
                "O planeta Terra é nosso! 🌍",
                "Não vais escapar! 👽",
                "A Terra será nossa! 👽",
                "Vamos apanhar-te! 😂"
            ]

            fala = random.choice(falas)

        alien = Alien(
            velocidade=velocidade,
            tamanho=tamanho,
            fala=fala
        )

        alien.vida = vida_alien
        alien.vida_maxima = vida_alien

        limite_x = max(
            1,
            int(
                Window.width
                - alien.width
            )
        )

        alien.x = random.randint(
            0,
            limite_x
        )

        alien.y = (
            Window.height
            + alien.height
        )

        self.inimigos.append(alien)

        self.aliens_layer.add_widget(
            alien
        )

    def limpar_aliens(self):

        for alien in self.inimigos[:]:
            self.remover_alien(alien)

    def criar_chefao(self):

        if self.nivel not in NIVEIS_CHEFOES:
            return

        if self.nivel in self.chefao_niveis_derrotados:
            return

        if self.chefao:
            return

        self.limpar_aliens()

        self.nave_chefao = NaveChefao(
            self.nivel
        )

        self.nave_chefao.x = (
            Window.width / 2
            - self.nave_chefao.width / 2
        )

        self.nave_chefao.y = (
            Window.height
            - self.nave_chefao.height
            - 85
        )

        self.nave_chefao_layer.add_widget(
            self.nave_chefao
        )

        self.chefao = Chefao(
            self.nivel
        )

        self.chefao.x = (
            Window.width / 2
            - self.chefao.width / 2
        )

        self.chefao.y = (
            self.nave_chefao.y
            - self.chefao.height
            + 20
        )

        self.chefao.saiu_da_nave = False

        self.chefao_layer.add_widget(
            self.chefao
        )

    def explosao_bomba_area(
        self,
        centro_x,
        centro_y
    ):

        explosao = Explosao(
            centro_x,
            centro_y,
            grande=True
        )

        self.explosoes_layer.add_widget(
            explosao
        )

        raio = 150
        aliens_atingidos = []

        for alien in self.inimigos[:]:

            distancia = math.sqrt(
                (alien.center_x - centro_x) ** 2
                +
                (alien.center_y - centro_y) ** 2
            )

            if distancia <= raio:
                aliens_atingidos.append(alien)

        for alien in aliens_atingidos:

            self.remover_alien(alien)
            self.pontos += 50

        if self.chefao:

            if self.chefao.saiu_da_nave:

                distancia = math.sqrt(
                    (self.chefao.center_x - centro_x) ** 2
                    +
                    (self.chefao.center_y - centro_y) ** 2
                )

                if distancia <= raio:

                    self.chefao.receber_dano(50)

                    self.pontos += 50

                    if self.chefao.vida <= 0:
                        self.derrotar_chefao()

        self.verificar_nivel()
        self.atualizar_hud()

    def atualizar(self, dt):

        if not self.inicio_pronto:
            return

        if self.pausado:
            return

        if self.jogo_terminou:
            return

        if self.tempo_recarga_fogo > 0:

            self.tempo_recarga_fogo -= dt

            if self.tempo_recarga_fogo < 0:
                self.tempo_recarga_fogo = 0

            self.atualizar_botao_fogo()

        for tiro in self.tiros[:]:

            tiro.y += 10
            tiro.animar(dt)

            if tiro.y > Window.height:
                self.remover_tiro(tiro)

        for bomba in self.bombas[:]:

            bomba.y += 7
            bomba.animar(dt)

            if bomba.y > Window.height:
                self.remover_bomba(bomba)

        for alien in self.inimigos[:]:

            alien.y -= alien.velocidade
            alien.animar_boca(dt)

            if self.colidiu(
                alien,
                self.jogador
            ):

                self.remover_alien(alien)

                self.vidas -= 1
                self.atualizar_hud()

                if self.vidas <= 0:
                    self.game_over()
                    return

                continue

            if alien.top < self.jogador.y:

                self.remover_alien(alien)

                self.vidas -= 1
                self.atualizar_hud()

                if self.vidas <= 0:
                    self.game_over()
                    return

        if self.nave_chefao:

            if self.chefao:

                self.chefao.animar_boca(dt)

                self.chefao.tempo_entrada += dt

                tempo = self.chefao.tempo_entrada

                restante = max(
                    0,
                    int(5 - tempo) + 1
                )

                if tempo < 5:

                    self.chefao.contagem.text = str(
                        restante
                    )

                    self.chefao.x = (
                        self.nave_chefao.center_x
                        - self.chefao.width / 2
                    )

                    self.chefao.y = (
                        self.nave_chefao.y
                        - self.chefao.height
                        + 20
                    )

                else:

                    self.chefao.contagem.text = ""

                    if not self.chefao.saiu_da_nave:

                        self.chefao.saiu_da_nave = True

                        self.chefao.y = (
                            self.nave_chefao.y
                            - self.chefao.height
                            - 5
                        )

        if self.chefao:

            if self.chefao.saiu_da_nave:

                self.chefao.y -= (
                    self.chefao.velocidade
                )

                self.chefao.x += (
                    self.chefao.velocidade
                    * 0.55
                    * self.chefao.direcao
                )

                if self.chefao.right >= Window.width:

                    self.chefao.right = Window.width
                    self.chefao.direcao = -1

                if self.chefao.x <= 0:

                    self.chefao.x = 0
                    self.chefao.direcao = 1

                if self.chefao.top < self.jogador.y:

                    self.vidas -= 1
                    self.atualizar_hud()

                    self.chefao.y = (
                        Window.height
                        - self.chefao.height
                        - 180
                    )

                    if self.vidas <= 0:
                        self.game_over()
                        return

                if self.colidiu(
                    self.chefao,
                    self.jogador
                ):

                    self.vidas -= 1
                    self.atualizar_hud()

                    self.chefao.y = (
                        Window.height
                        - self.chefao.height
                        - 180
                    )

                    if self.vidas <= 0:
                        self.game_over()
                        return

        for tiro in self.tiros[:]:

            atingiu = False

            for alien in self.inimigos[:]:

                if self.colidiu(
                    tiro,
                    alien
                ):

                    self.remover_tiro(tiro)

                    alien.vida -= 1

                    if alien.vida <= 0:

                        explosao = Explosao(
                            alien.center_x,
                            alien.center_y
                        )

                        self.explosoes_layer.add_widget(
                            explosao
                        )

                        self.remover_alien(alien)

                        self.pontos += 10

                        self.verificar_nivel()

                    self.atualizar_hud()

                    atingiu = True

                    break

            if atingiu:
                continue

            if self.chefao:

                if not self.chefao.saiu_da_nave:
                    continue

                if self.colidiu(
                    tiro,
                    self.chefao
                ):

                    self.remover_tiro(tiro)

                    self.chefao.receber_dano(10)

                    self.pontos += 10

                    if self.chefao.vida <= 0:
                        self.derrotar_chefao()

                    self.atualizar_hud()

        for bomba in self.bombas[:]:

            atingiu = False

            for alien in self.inimigos[:]:

                if self.colidiu(
                    bomba,
                    alien
                ):

                    centro_x = bomba.center_x
                    centro_y = bomba.center_y

                    self.remover_bomba(bomba)

                    self.explosao_bomba_area(
                        centro_x,
                        centro_y
                    )

                    atingiu = True

                    break

            if atingiu:
                continue

            if self.chefao:

                if not self.chefao.saiu_da_nave:
                    continue

                if self.colidiu(
                    bomba,
                    self.chefao
                ):

                    centro_x = bomba.center_x
                    centro_y = bomba.center_y

                    self.remover_bomba(bomba)

                    self.explosao_bomba_area(
                        centro_x,
                        centro_y
                    )

    def derrotar_chefao(self):

        if not self.chefao:
            return

        nivel_derrotado = self.chefao.nivel

        explosao = Explosao(
            self.chefao.center_x,
            self.chefao.center_y,
            grande=True
        )

        self.explosoes_layer.add_widget(
            explosao
        )

        self.chefao_niveis_derrotados.add(
            nivel_derrotado
        )

        if self.chefao.parent:

            self.chefao.parent.remove_widget(
                self.chefao
            )

        self.chefao = None

        if self.nave_chefao:

            if self.nave_chefao.parent:

                self.nave_chefao.parent.remove_widget(
                    self.nave_chefao
                )

            self.nave_chefao = None

        if nivel_derrotado == 60:

            self.pontos = 60000
            self.nivel = 60

            self.atualizar_hud()

            self.jogo_concluido = True
            self.jogo_terminou = True

            self.salvar_recorde()

            self.parar_relogios()

            Clock.schedule_once(
                lambda dt:
                self.mostrar_creditos_finais(),
                0.5
            )

            return

        self.pontos += 300

        self.atualizar_hud()
        self.salvar_recorde()

    def colidiu(
        self,
        objeto1,
        objeto2
    ):

        return (
            objeto1.x < objeto2.right
            and objeto1.right > objeto2.x
            and objeto1.y < objeto2.top
            and objeto1.top > objeto2.y
        )

    def remover_alien(self, alien):

        if alien in self.inimigos:
            self.inimigos.remove(alien)

        if alien.parent:
            alien.parent.remove_widget(alien)

    def remover_tiro(self, tiro):

        if tiro in self.tiros:
            self.tiros.remove(tiro)

        if tiro.parent:
            tiro.parent.remove_widget(tiro)

    def remover_bomba(self, bomba):

        if bomba in self.bombas:
            self.bombas.remove(bomba)

        if bomba.parent:
            bomba.parent.remove_widget(bomba)

    def verificar_nivel(self):

        novo_nivel = (
            self.pontos // 1000
        ) + 1

        if novo_nivel > 60:
            novo_nivel = 60

        if novo_nivel > self.nivel:

            self.nivel = novo_nivel

            self.fundo.velocidade = min(
                10,
                2
                + (self.nivel - 1) * 10
            )

            self.atualizar_hud()

            if self.nivel in NIVEIS_CHEFOES:
                self.criar_chefao()

    def atualizar_hud(self):

        self.label_pontos.text = (
            "Pontos: "
            + str(self.pontos)
        )

        self.label_nivel.text = (
            "Nivel: "
            + str(self.nivel)
        )

        self.label_recorde.text = (
            "Recorde: "
            + str(self.ler_recorde())
        )

        if self.vidas > 0:

            self.label_vidas.text = (
                "❤️" * self.vidas
            )

        else:

            self.label_vidas.text = ""

    def ler_recorde(self):

        try:

            if os.path.exists(
                ARQUIVO_RECORDE
            ):

                with open(
                    ARQUIVO_RECORDE,
                    "r"
                ) as arquivo:

                    return int(
                        arquivo.read().strip()
                    )

        except:
            pass

        return 0

    def salvar_recorde(self):

        recorde = self.ler_recorde()

        if self.pontos > recorde:

            try:

                with open(
                    ARQUIVO_RECORDE,
                    "w"
                ) as arquivo:

                    arquivo.write(
                        str(self.pontos)
                    )

            except:
                pass

    def game_over(self):

        if self.jogo_terminou:
            return

        self.jogo_terminou = True

        self.salvar_recorde()

        self.overlay = Widget()

        with self.overlay.canvas:

            Color(
                0,
                0,
                0,
                0.75
            )

            self.overlay_fundo = Rectangle(
                pos=(0, 0),
                size=Window.size
            )

        self.add_widget(self.overlay)

        painel = BoxLayout(
            orientation="vertical",
            spacing=15,
            padding=25,
            size_hint=(
                None,
                None
            ),
            size=(
                300,
                330
            ),
            pos=(
                Window.width / 2 - 150,
                Window.height / 2 - 165
            )
        )

        with painel.canvas.before:

            Color(
                0.04,
                0.05,
                0.15,
                1
            )

            painel_fundo = RoundedRectangle(
                pos=painel.pos,
                size=painel.size,
                radius=[25]
            )

        painel.bind(
            pos=lambda obj, value:
            setattr(
                painel_fundo,
                "pos",
                value
            ),
            size=lambda obj, value:
            setattr(
                painel_fundo,
                "size",
                value
            )
        )

        titulo = Label(
            text="FIM DE JOGO",
            color=VERMELHO,
            bold=True,
            font_size=26
        )

        pontos = Label(
            text=(
                "Pontos: "
                + str(self.pontos)
            ),
            color=BRANCO,
            font_size=20
        )

        recorde = Label(
            text=(
                "Recorde: "
                + str(self.ler_recorde())
            ),
            color=AMARELO,
            font_size=18
        )

        botao_novamente = BotaoJogo(
            text="JOGAR NOVAMENTE",
            cor=VERDE
        )

        botao_menu = BotaoJogo(
            text="MENU",
            cor=AZUL
        )

        botao_sair = BotaoJogo(
            text="SAIR DO JOGO",
            cor=VERMELHO
        )

        botao_novamente.bind(
            on_press=lambda *args:
            self.novo_jogo_callback()
        )

        botao_menu.bind(
            on_press=lambda *args:
            self.menu_callback()
        )

        botao_sair.bind(
            on_press=lambda *args:
            App.get_running_app().stop()
        )

        painel.add_widget(titulo)
        painel.add_widget(pontos)
        painel.add_widget(recorde)
        painel.add_widget(botao_novamente)
        painel.add_widget(botao_menu)
        painel.add_widget(botao_sair)

        self.add_widget(painel)

    def mostrar_creditos_finais(self):

        for alien in self.inimigos[:]:
            self.remover_alien(alien)

        for tiro in self.tiros[:]:
            self.remover_tiro(tiro)

        for bomba in self.bombas[:]:
            self.remover_bomba(bomba)

        if self.chefao:

            if self.chefao.parent:
                self.chefao.parent.remove_widget(
                    self.chefao
                )

            self.chefao = None

        if self.nave_chefao:

            if self.nave_chefao.parent:
                self.nave_chefao.parent.remove_widget(
                    self.nave_chefao
                )

            self.nave_chefao = None

        self.overlay_final = Widget()

        with self.overlay_final.canvas:

            Color(
                0,
                0,
                0,
                0.88
            )

            self.overlay_final_fundo = Rectangle(
                pos=(0, 0),
                size=Window.size
            )

        self.add_widget(
            self.overlay_final
        )

        painel = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=[
                20,
                20
            ],
            size_hint=(
                0.88,
                0.78
            ),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.50
            }
        )

        with painel.canvas.before:

            Color(
                0.04,
                0.05,
                0.15,
                1
            )

            painel_fundo = RoundedRectangle(
                pos=painel.pos,
                size=painel.size,
                radius=[25]
            )

        painel.bind(
            pos=lambda obj, value:
            setattr(
                painel_fundo,
                "pos",
                value
            ),
            size=lambda obj, value:
            setattr(
                painel_fundo,
                "size",
                value
            )
        )

        titulo = Label(
            text="SPACE ATTACK",
            color=AMARELO,
            bold=True,
            font_size=30,
            size_hint_y=None,
            height=55
        )

        painel.add_widget(titulo)

        concluido = Label(
            text="JOGO CONCLUÍDO",
            color=VERDE,
            bold=True,
            font_size=24,
            size_hint_y=None,
            height=45
        )

        painel.add_widget(concluido)

        creditos = Label(
            text=(
                "Parabéns!\n"
                "Concluíste todos os 60 níveis.\n\n"
                "────────────────────\n\n"
                "CRÉDITOS\n\n"
                "Este jogo foi criado por\n"
                "ZEFFERINO TOMÁS\n"
                "Conhecido como WIZKHAY\n\n"
                "Desenvolvido com\n"
                "PYTHON + KIVY\n\n"
                "────────────────────\n\n"
                "PERSONAGEM PRINCIPAL\n\n"
                "EBENESIS\n\n"
                "O personagem principal deste jogo\n"
                "é Ebenesis, filho de Zeferino Tomás."
            ),
            color=BRANCO,
            font_size=15,
            halign="center",
            valign="middle"
        )

        creditos.bind(
            size=lambda obj, value:
            setattr(
                obj,
                "text_size",
                value
            )
        )

        painel.add_widget(creditos)

        botao_novamente = BotaoJogo(
            text="JOGAR NOVAMENTE",
            cor=VERDE,
            size_hint_y=None,
            height=50
        )

        botao_novamente.bind(
            on_press=lambda *args:
            self.novo_jogo_callback()
        )

        painel.add_widget(
            botao_novamente
        )

        botao_menu = BotaoJogo(
            text="MENU",
            cor=AZUL,
            size_hint_y=None,
            height=50
        )

        botao_menu.bind(
            on_press=lambda *args:
            self.menu_callback()
        )

        painel.add_widget(
            botao_menu
        )

        self.add_widget(painel)

    def parar_relogios(self):

        Clock.unschedule(self.atualizar)
        Clock.unschedule(self.criar_inimigo)
        Clock.unschedule(self.atirar_automaticamente)
        Clock.unschedule(self.iniciar_jogo)
        Clock.unschedule(self.fundo.animar_estrelas)


# =========================================================
# TELA DO JOGO
# =========================================================

class TelaJogo(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.jogo = None

    def on_enter(self):

        self.novo_jogo()

    def novo_jogo(self, *args):

        if self.jogo:
            self.jogo.parar_relogios()

        self.clear_widgets()

        self.jogo = Jogo(
            novo_jogo_callback=self.novo_jogo,
            menu_callback=self.ir_menu
        )

        self.add_widget(self.jogo)

    def ir_menu(self, *args):

        if self.jogo:
            self.jogo.parar_relogios()

        self.manager.current = "inicio"


# =========================================================
# TELA DE CARREGAMENTO
# =========================================================

class TelaCarregando(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        layout = FloatLayout()

        if os.path.exists(CARTAZ_IMG):

            try:

                textura = CoreImage(
                    CARTAZ_IMG
                ).texture

                with layout.canvas.before:

                    Color(
                        1,
                        1,
                        1,
                        1
                    )

                    self.cartaz = Rectangle(
                        texture=textura,
                        pos=(0, 0),
                        size=Window.size
                    )

                layout.bind(
                    size=self.atualizar_cartaz,
                    pos=self.atualizar_cartaz
                )

            except Exception as erro:

                mensagem_erro = Label(
                    text=(
                        "ERRO AO CARREGAR cartaz.png\n\n"
                        + str(erro)
                    ),
                    color=VERMELHO,
                    bold=True,
                    font_size=16,
                    halign="center",
                    valign="middle",
                    size_hint=(1, 1)
                )

                mensagem_erro.bind(
                    size=lambda obj, value:
                    setattr(
                        obj,
                        "text_size",
                        value
                    )
                )

                layout.add_widget(
                    mensagem_erro
                )

        else:

            mensagem_erro = Label(
                text=(
                    "cartaz.png NÃO FOI ENCONTRADO\n\n"
                    "Local esperado:\n\n"
                    + CARTAZ_IMG
                ),
                color=VERMELHO,
                bold=True,
                font_size=18,
                halign="center",
                valign="middle",
                size_hint=(1, 1)
            )

            mensagem_erro.bind(
                size=lambda obj, value:
                setattr(
                    obj,
                    "text_size",
                    value
                )
            )

            layout.add_widget(
                mensagem_erro
            )

        texto = Label(
            text="CARREGANDO, POR FAVOR AGUARDE...",
            color=BRANCO,
            bold=True,
            font_size=18,
            size_hint=(
                1,
                None
            ),
            height=50,
            pos_hint={
                "x": 0,
                "y": 0.03
            }
        )

        layout.add_widget(texto)

        self.add_widget(layout)

        self.evento_carregamento = None

    def on_enter(self, *args):

        if self.evento_carregamento:
            self.evento_carregamento.cancel()

        self.evento_carregamento = Clock.schedule_once(
            self.ir_para_menu,
            15
        )

    def atualizar_cartaz(self, *args):

        if hasattr(
            self,
            "cartaz"
        ):

            self.cartaz.pos = (
                0,
                0
            )

            self.cartaz.size = (
                Window.width,
                Window.height
            )

    def ir_para_menu(self, dt):

        if self.manager:
            self.manager.current = "inicio"


# =========================================================
# TELA INICIAL
# =========================================================

class TelaInicial(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        layout = FloatLayout()

        fundo = FundoEspacial()

        layout.add_widget(fundo)

        titulo = Label(
            text="SPACE ATTACK",
            font_size=34,
            bold=True,
            color=BRANCO,
            size_hint=(
                1,
                None
            ),
            height=60,
            pos_hint={
                "center_x": 0.5,
                "top": 0.90
            }
        )

        layout.add_widget(titulo)

        if os.path.exists(JOGADOR_IMG):

            imagem = Image(
                source=JOGADOR_IMG,
                size_hint=(
                    None,
                    None
                ),
                size=(
                    180,
                    300
                ),
                pos_hint={
                    "center_x": 0.5,
                    "center_y": 0.68
                },
                allow_stretch=True,
                keep_ratio=True
            )

            layout.add_widget(imagem)

        subtitulo = Label(
            text="DEFENDA O ESPAÇO",
            font_size=17,
            color=BRANCO,
            size_hint=(
                1,
                None
            ),
            height=20,
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.54
            }
        )

        layout.add_widget(subtitulo)

        botao_comecar = BotaoJogo(
            text="COMEÇAR",
            cor=VERDE,
            size_hint=(
                None,
                None
            ),
            size=(
                250,
                55
            ),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.43
            }
        )

        botao_como = BotaoJogo(
            text="COMO JOGAR",
            cor=AZUL,
            size_hint=(
                None,
                None
            ),
            size=(
                250,
                55
            ),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.33
            }
        )

        botao_recorde = BotaoJogo(
            text="RECORDE",
            cor=ROXO,
            size_hint=(
                None,
                None
            ),
            size=(
                250,
                55
            ),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.23
            }
        )

        botao_sair = BotaoJogo(
            text="SAIR DO JOGO",
            cor=VERMELHO,
            size_hint=(
                None,
                None
            ),
            size=(
                250,
                55
            ),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.13
            }
        )

        botao_comecar.bind(
            on_press=self.comecar
        )

        botao_como.bind(
            on_press=self.como_jogar
        )

        botao_recorde.bind(
            on_press=self.ver_recorde
        )

        botao_sair.bind(
            on_press=self.sair
        )

        layout.add_widget(botao_comecar)
        layout.add_widget(botao_como)
        layout.add_widget(botao_recorde)
        layout.add_widget(botao_sair)

        self.add_widget(layout)

    def comecar(self, *args):

        self.manager.current = "jogo"

    def como_jogar(self, *args):

        self.manager.current = "instruçoes"

    def ver_recorde(self, *args):

        self.manager.current = "recorde"

    def sair(self, *args):

        App.get_running_app().stop()


# =========================================================
# INSTRUÇÕES
# =========================================================

class TelaInstrucoes(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        layout = FloatLayout()

        fundo = FundoEspacial()

        layout.add_widget(fundo)

        titulo = Label(
            text="COMO JOGAR",
            font_size=30,
            bold=True,
            color=BRANCO,
            size_hint=(
                1,
                None
            ),
            height=60,
            pos_hint={
                "top": 0.92
            }
        )

        layout.add_widget(titulo)

        texto = Label(
            text=(
                "Use os botoes ESQUERDA e DIREITA "
                "para mover a nave.\n\n"
                "A nave dispara automaticamente "
                "pela pistola esquerda.\n\n"
                "O botao FOGO lança uma BOMBA "
                "especial.\n\n"
                "A bomba cria uma grande explosão "
                "que pode atingir vários adversários "
                "ao mesmo tempo.\n\n"
                "A bomba causa 50 de dano aos chefões.\n\n"
                "Depois de usar o FOGO, ele precisa "
                "de 5 segundos para recarregar.\n\n"
                "Destrua os aliens para ganhar pontos.\n\n"
                "Quanto maior o nivel, mais resistentes "
                "ficam os aliens.\n\n"
                "A cada 1000 pontos o nivel aumenta.\n\n"
                "Os chefões aparecem nos niveis "
                "5, 10, 20, 30, 40, 50 e 60.\n\n"
                "Cada chefão é maior e diferente "
                "dos aliens normais.\n\n"
                "A nave do chefão aparece primeiro.\n\n"
                "O chefão fica 5 segundos parado "
                "antes de sair da nave.\n\n"
                "Depois começa a descer.\n\n"
                "Os chefões possuem muita vida e "
                "precisam de muitos disparos.\n\n"
                "O nível 60 possui o CHEFÃO FINAL.\n\n"
                "A nave começa com 5 vidas."
            ),
            color=BRANCO,
            font_size=15,
            halign="center",
            valign="middle",
            size_hint=(
                0.88,
                0.73
            ),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.54
            }
        )

        texto.bind(
            size=lambda obj, value:
            setattr(
                obj,
                "text_size",
                value
            )
        )

        layout.add_widget(texto)

        voltar = BotaoJogo(
            text="VOLTAR",
            cor=AZUL,
            size_hint=(
                None,
                None
            ),
            size=(
                220,
                55
            ),
            pos_hint={
                "center_x": 0.5,
                "y": 0.05
            }
        )

        voltar.bind(
            on_press=lambda *args:
            setattr(
                self.manager,
                "current",
                "inicio"
            )
        )

        layout.add_widget(voltar)

        self.add_widget(layout)


# =========================================================
# RECORDE
# =========================================================

class TelaRecorde(Screen):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.layout = FloatLayout()

        fundo = FundoEspacial()

        self.layout.add_widget(fundo)

        titulo = Label(
            text="RECORDE",
            font_size=32,
            bold=True,
            color=AMARELO,
            size_hint=(
                1,
                None
            ),
            height=60,
            pos_hint={
                "top": 0.90
            }
        )

        self.layout.add_widget(titulo)

        self.label_recorde = Label(
            text="0",
            font_size=45,
            bold=True,
            color=BRANCO,
            size_hint=(
                1,
                None
            ),
            height=70,
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.58
            }
        )

        self.layout.add_widget(
            self.label_recorde
        )

        voltar = BotaoJogo(
            text="VOLTAR",
            cor=AZUL,
            size_hint=(
                None,
                None
            ),
            size=(
                220,
                55
            ),
            pos_hint={
                "center_x": 0.5,
                "y": 0.12
            }
        )

        voltar.bind(
            on_press=lambda *args:
            setattr(
                self.manager,
                "current",
                "inicio"
            )
        )

        self.layout.add_widget(voltar)

        self.add_widget(self.layout)

    def on_pre_enter(self):

        recorde = 0

        try:

            if os.path.exists(
                ARQUIVO_RECORDE
            ):

                with open(
                    ARQUIVO_RECORDE,
                    "r"
                ) as arquivo:

                    recorde = int(
                        arquivo.read().strip()
                    )

        except:

            recorde = 0

        self.label_recorde.text = str(
            recorde
        )


# =========================================================
# APP
# =========================================================

class SpaceAttackApp(App):

    def preparar_pasta_da_aplicacao(self):
        """Usa recursos incluídos no APK e guarda o recorde em pasta gravável."""
        global PASTA, JOGADOR_IMG, SOM_DISPARO, ARQUIVO_RECORDE, CARTAZ_IMG

        # Imagens e som são recursos só de leitura, incluídos com o main.py.
        pasta_codigo = os.path.dirname(os.path.abspath(__file__))
        JOGADOR_IMG = os.path.join(pasta_codigo, "jogador.png")
        SOM_DISPARO = os.path.join(pasta_codigo, "disparo.mp3")
        CARTAZ_IMG = os.path.join(pasta_codigo, "cartaz.png")

        # O recorde precisa de uma pasta onde a aplicação possa escrever.
        PASTA = self.user_data_dir
        os.makedirs(PASTA, exist_ok=True)
        ARQUIVO_RECORDE = os.path.join(PASTA, "recorde_jogo.txt")

    def build(self):

        self.preparar_pasta_da_aplicacao()

        gerenciador = ScreenManager(
            transition=FadeTransition(
                duration=0.25
            )
        )

        tela_carregando = TelaCarregando(
            name="carregando"
        )

        tela_inicio = TelaInicial(
            name="inicio"
        )

        tela_instrucoes = TelaInstrucoes(
            name="instruçoes"
        )

        tela_recorde = TelaRecorde(
            name="recorde"
        )

        tela_jogo = TelaJogo(
            name="jogo"
        )

        gerenciador.add_widget(
            tela_carregando
        )

        gerenciador.add_widget(
            tela_inicio
        )

        gerenciador.add_widget(
            tela_instrucoes
        )

        gerenciador.add_widget(
            tela_recorde
        )

        gerenciador.add_widget(
            tela_jogo
        )

        gerenciador.current = "carregando"

        return gerenciador


# =========================================================
# EXECUTAR
# =========================================================

if __name__ == "__main__":

    SpaceAttackApp().run()
