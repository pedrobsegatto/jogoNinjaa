import pygame
import random
import os
from tkinter import simpledialog

pygame.init()

relogio = pygame.time.Clock()
icone  = pygame.image.load("recursos/icone.png")
ninja = pygame.image.load("recursos/ninja.png")
fundo = pygame.image.load("recursos/fundo.png")
fundoStart = pygame.image.load("recursos/fundoStart.jpg")
fundoDead = pygame.image.load("recursos/fundoDead.png")
fundoCachaca = pygame.image.load("recursos/fundoCachaca")

cachaca = pygame.image.load("recursos/cachaca.png")
moeda = pygame.image.load("recursos/moeda.png")
tamanho = (800,600)
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("PAGUE O NINJA")
pygame.display.set_icon(icone)
moedaSound = pygame.mixer.Sound("recursos/moeda.mp3")
morteSound = pygame.mixer.Sound("recursos/morte.mp3")
morteCachaca = pygame.mixer.Sound("recursos/morteCachaca.mp3")
fonte = pygame.font.SysFont("comicsans",28)
fonteStart = pygame.font.SysFont("comicsans",55)
fonteMorte = pygame.font.SysFont("arial",120)
pygame.mixer.music.load("recursos/musica.mp3")

branco = (255,255,255)
preto = (0, 0 ,0 )
vermelho = (160,0,0)

def jogar(nome):
    pygame.mixer.Sound.play(moedaSound)
    pygame.mixer.music.play(-1)
    posicaoXNinja = 400
    posicaoYNinja = 600
    movimentoXNinja  = 0
    movimentoYNinja  = 0
    posicaoXmoeda = 400
    posicaoYmoeda = -240
    velocidademoeda = 1
    pontos = 0
    larguraNinja = 137
    alturaNinja = 158
    larguamoeda  = 87
    alturamoeda  = 87
    dificuldade  = 20

    posicaoXCachaca = 400
    posicaoYCachaca = -240
    velocidadeCachaca = 2
    larguaCachaca  = 112
    alturaCachaca  = 112


    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXNinja = 10
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXNinja = -10
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXNinja = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXNinja = 0
                
        posicaoXNinja = posicaoXNinja + movimentoXNinja            
        posicaoYNinja = posicaoYNinja + movimentoYNinja            
        
        if posicaoXNinja < 0 :
            posicaoXNinja = 10
        elif posicaoXNinja >550:
            posicaoXNinja = 540
            
        if posicaoYNinja < 0 :
            posicaoYNinja = 10
        elif posicaoYNinja > 473:
            posicaoYNinja = 463
        
        tela.fill(branco)
        tela.blit(fundo, (0,0) )
        #pygame.draw.circle(tela, preto, (posicaoXNinja,posicaoYNinja), 40, 0 )
        tela.blit( ninja, (posicaoXNinja, posicaoYNinja) )
        
        posicaoYmoeda = posicaoYmoeda + velocidademoeda
        if posicaoYmoeda > 600:
            posicaoYmoeda = -240
            pontos = pontos + 1
            velocidademoeda = velocidademoeda + 1
            posicaoXmoeda = random.randint(0,800)
            pygame.mixer.Sound.play(moedaSound)

        tela.blit( moeda, (posicaoXmoeda, posicaoYmoeda) )

        posicaoYCachaca = posicaoYCachaca + velocidadeCachaca
        if posicaoYCachaca > 600:
            posicaoYCachaca = -240
            pontos = pontos + 1
            velocidadeCachaca = velocidadeCachaca + 1
            posicaoXCachaca = random.randint(0,800)
            pygame.mixer.Sound.play(moedaSound)
        
        tela.blit( cachaca, (posicaoXCachaca, posicaoYCachaca) )
            
        if posicaoXCachaca == posicaoXNinja and posicaoYCachaca == posicaoYNinja:
            pontos + 1
            
        
        
        texto = fonte.render(nome+"- Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (10,10))
        
        pixelsNinjaX = list(range(posicaoXNinja, posicaoXNinja+larguraNinja))
        pixelsNinjaY = list(range(posicaoYNinja, posicaoYNinja+alturaNinja))
        pixelsmoedaX = list(range(posicaoXmoeda, posicaoXmoeda + larguamoeda))
        pixelsmoedaY = list(range(posicaoYmoeda, posicaoYmoeda + alturamoeda))
        pixelsCachacaX = list(range(posicaoXCachaca, posicaoXCachaca + larguaCachaca))
        pixelsCachacaY = list(range(posicaoYCachaca, posicaoYCachaca + alturaCachaca))
        
        #print( len( list( set(pixelsmoedaX).intersection(set(pixelsNinjaX))   ) )   )
        if  len( list( set(pixelsmoedaY).intersection(set(pixelsNinjaY))) ) > dificuldade:
            if len( list( set(pixelsmoedaX).intersection(set(pixelsNinjaX))   ) )  > dificuldade:
                dead(nome, pontos)
        
        if  len( list( set(pixelsCachacaY).intersection(set(pixelsNinjaY))) ) > dificuldade:
            if len( list( set(pixelsCachacaX).intersection(set(pixelsNinjaX))   ) )  > dificuldade:
                deadCachaca(nome, pontos)
        
        pygame.display.update()
        relogio.tick(60)

def deadCachaca(nome, pontos):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(morteCachaca)
    
    jogadas  = {}
    try:
        arquivo = open("historico.txt","r",encoding="utf-8")
        jogadas = eval(arquivo.read())
        arquivo.close()
    except:
        arquivo = open("historico.txt","w",encoding="utf-8")
        arquivo.close()
 
    jogadas[nome] = pontos   
    arquivo = open("historico.txt","w",encoding="utf-8") 
    arquivo.write(str(jogadas))
    arquivo.close()
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                jogar(nome)

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
        tela.fill(branco)
        tela.blit(fundoCachaca, (0,0))
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
        textoStart = fonteStart.render("",True, branco)
        tela.blit(textoStart, (400,482))
        textoEnter = fonte.render("Ninja entrou em coma alcoólico, precione ENTER e tente novamente...", True, vermelho)
        tela.blit(textoEnter, (60,482))
        pygame.display.update()
        relogio.tick(60)

def dead(nome, pontos):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(morteSound)
    
    jogadas  = {}
    try:
        arquivo = open("historico.txt","r",encoding="utf-8")
        jogadas = eval(arquivo.read())
        arquivo.close()
    except:
        arquivo = open("historico.txt","w",encoding="utf-8")
        arquivo.close()
 
    jogadas[nome] = pontos   
    arquivo = open("historico.txt","w",encoding="utf-8") 
    arquivo.write(str(jogadas))
    arquivo.close()
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                jogar(nome)

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
        tela.fill(branco)
        tela.blit(fundoDead, (0,0))
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
        textoStart = fonteStart.render("",True, branco)
        tela.blit(textoStart, (400,482))
        textoEnter = fonte.render("Pressione ENTER para buscar vingança...", True, vermelho)
        tela.blit(textoEnter, (60,482))
        pygame.display.update()
        relogio.tick(60)

def ranking():
    estrelas = {}
    try:
        arquivo = open("historico.txt","r",encoding="utf-8" )
        estrelas = eval(arquivo.read())
        arquivo.close()
    except:
        pass
    
    nomes = sorted(estrelas, key=estrelas.get,reverse=True)
    print(estrelas)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    start()

        tela.fill(preto)
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
        textoStart = fonteStart.render("BACK TO START", True, branco)
        tela.blit(textoStart, (330,482))
        
        posicaoY = 50
        for key,nome in enumerate(nomes):
            if key == 13:
                break
            textoJogador = fonte.render(nome + " - "+str(estrelas[nome]), True, branco)
            tela.blit(textoJogador, (300,posicaoY))
            posicaoY = posicaoY + 30

        pygame.display.update()
        relogio.tick(60)

def start():
    nome = simpledialog.askstring("Ninja","CPF:")
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
                elif buttonRanking.collidepoint(evento.pos):
                    ranking()

        tela.fill(branco)
        tela.blit(fundoStart, (0,0))
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
        buttonRanking = pygame.draw.rect(tela, preto, (35,50,200,50),0,30)
        textoRanking = fonte.render("Ranking", True, branco)
        tela.blit(textoRanking, (90,50))
        textoStart = fonteStart.render("START", True, branco)
        tela.blit(textoStart, (330,482))
 
        pygame.display.update()
        relogio.tick(60)

start()