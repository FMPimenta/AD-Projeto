#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_pool.py
Grupo: 3 
Membros: Francisco Pimenta 54973, Pedro Quintão 54971 
"""

import time

###############################################################################

class resource_lock:
    def __init__(self, resource_id):
        """
        Define e inicializa as características de um LOCK num recurso.
        """
        self.id = resource_id
        self.estado = "UNLOCKED"
        self.bloqueios = 0
        self.clientID = -1
        self.lockedTime = 0

    def lock(self, client_id, time_limit):
        """
        Tenta bloquear o recurso pelo cliente client_id, durante time_limit 
        segundos. Retorna OK ou NOK.
        """
        if (self.status("R") == "UNLOCKED"):
            self.estado = "LOCKED"
            self.bloqueios += 1
            self.clientID = client_id
            self.lockedTime = (time.time()) + time_limit
            return True
        elif (self.status("R") == "LOCKED"):
            if (self.clientID == client_id):
                self.bloqueios += 1
                self.lockedTime += time_limit
                return True
            else:
                return False
        else:
            return False

    def release(self):
        """
        Liberta o recurso incondicionalmente, alterando os valores associados
        ao bloqueio.
        """
        self.estado = "UNLOCKED"
        #self.bloqueios = 0
        self.lockedTime = 0

    def unlock(self, client_id):
        """
        Liberta o recurso se este está bloqueado pelo cliente client_id.
        Retorna OK ou NOK.
        """

        if (self.status("R") == "LOCKED" and self.clientID == client_id):
            self.release()
            return True
        else:
            return False

    def status(self, option):
        """
        Obtém o estado do recurso. Se option for R, retorna LOCKED ou UNLOCKED 
        ou DISABLED. Se option for K, retorna <número de bloqueios feitos no 
        recurso>.
        """
        if (option == "R"):
            return self.estado
        elif (option == "K"):
            return self.bloqueios

    def disable(self):
        """
        Coloca o recurso como desabilitdado incondicionalmente, alterando os 
        valores associados à sua disponibilidade.
        """
        self.estado = Ellipsis

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print ou str.
        """
        output = ""
        # Se o recurso está bloqueado:
        # R <número do recurso> bloqueado <id do cliente> <instante limite da
        #concessão do bloqueio>
        if (self.status("R") == "LOCKED"):
            output = "R %s bloqueado %s %s" % (
                self.id, self.clientID, self.lockedTime)
        # Se o recurso está desbloquado:
        # R <número do recurso> desbloqueado
        elif (self.status("R") == "UNLOCKED"):
            output = "R %s desbloqueado" % self.id
        # Se o recurso está inativo:
        # R <número do recurso> inativo
        else:
            output = "R %s inativo" % self.id
        return output

###############################################################################


class lock_pool:
    def __init__(self, N, K, Y):
        """
        Define um array com um conjunto de locks para N recursos. Os locks podem
        ser manipulados pelos métodos desta classe. Define K, o número máximo 
        de bloqueios permitidos para cada recurso. Ao atingir K, o recurso fica 
        desabilitdado. Define Y, o número máximo permitido de recursos 
        bloqueados num dado momento. Ao atingir Y, não é possível realizar mais 
        bloqueios até que um recurso seja libertado.
        """
        self.N = N
        self.K = K
        self.Y = Y

        self.resources = []
        for i in range(self.N):
            self.resources.append(resource_lock(i))

    def clear_expired_locks(self):
        """
        Verifica se os recursos que estão bloqueados ainda estão dentro do tempo
        de concessão dos bloqueios. Remove os bloqueios para os quais o tempo de
        concessão tenha expirado.
        """
        for r in self.resources:
            #if (r.status("R") == "LOCKED" or r.status("R") == "DISABLED") and r.lockedTime < time.time():
            #r.release()
            if (r.status("R") == "LOCKED" and r.lockedTime < time.time()):
                r.release()

    def lock(self, resource_id, client_id, time_limit):
        """
        Tenta bloquear o recurso resource_id pelo cliente client_id, durante
        time_limit segundos. Retorna OK, NOK ou UNKNOWN RESOURCE.
        """
        if (resource_id < 0 or resource_id > self.N - 1):
            return None
        elif (self.status("K", resource_id) < self.K and self.stats("Y") < self.Y):
            return self.resources[resource_id].lock(client_id, time_limit)
        else:
            return False

    def unlock(self, resource_id, client_id):
        """
        Liberta o bloqueio sobre o recurso resource_id pelo cliente client_id.
        Retorna OK, NOK ou UNKNOWN RESOURCE.
        """
        if (resource_id < 0 or resource_id > self.N - 1):
            return None
        else:
            return self.resources[resource_id].unlock(client_id)

    def status(self, option, resource_id):
        """
        Obtém o estado de um recurso. Se option for R, retorna LOCKED, UNLOCKED,
        DISABLED ou UNKNOWN RESOURCE. Se option for K, retorna <número de 
        bloqueios feitos no recurso> ou UNKNOWN RESOURCE.
        """
        if resource_id < 0 or resource_id >= len(self.resources):
            return None
        else:
            return self.resources[resource_id].status(option)

    def stats(self, option):
        """
        Obtém o estado do serviço de exclusão mútua. Se option for Y, retorna 
        <número de recursos bloqueados atualmente>. Se option for N, retorna 
        <número de recursos disponiveis atualmente>. Se option for D, retorna 
        <número de recursos desabilitdados>
        """
        lockedResources = 0
        unlockedResources = 0
        disabledResources = 0

        for r in self.resources:
            if (r.status("R") == "LOCKED"):
                lockedResources += 1
            elif (r.status("R") == "UNLOCKED"):
                unlockedResources += 1
            else:
                disabledResources += 1

        if (option == "Y"):
            return lockedResources
        elif (option == "N"):
            return unlockedResources
        elif (option == "D"):
            return disabledResources

    def disable_resources(self):
        """
        Verifica se os recursos que estão bloqueados já atingiram o número de
        bloqueios permitidos e desativa esses recursos em caso positivo.
        """

        for r in self.resources:
            if r.status("R") != Ellipsis and r.bloqueios >= self.K:
                r.disable()

    def __repr__(self):
        """
        Representação da classe para a saída standard. A string devolvida por
        esta função é usada, por exemplo, se uma instância da classe for
        passada à função print ou str.
        """
        output = ""
        #
        # Acrescentar no output uma linha por cada recurso
        #
        for r in self.resources:
            if r.status("R") != "LOCKED":
                output += "R %s %s %s " % (r.id, r.status("R"), r.status("K"))
            else:
                output += "R %s %s %s %s %s " % \
                    (r.id, r.status("R"), r.status("K"), r.clientID, r.lockedTime)

        return output

###############################################################################
