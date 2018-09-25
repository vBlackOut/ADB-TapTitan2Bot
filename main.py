from Actions.attackTitan import Actions

if __name__ == "__main__":
    Titan = Actions()
    while 1:
        Titan.defaultAttackTitan(250) # number tap for attack Titan
        Titan.upgradeHeros(25) # <- number loop for upgrade heros
        Titan.bossAttack() # click on attack Boss
        # end loop to restart attackTitan again.
