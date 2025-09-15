#Code des Catastrofes visualisatie
#Deze code gebruikt erg veel modules, deze moeten geïnstalleerd zijn om de code te kunnen uitvoeren. Verder moet de map "my-models" aanwezig zijn in de werkdirectory.
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import AmbientLight, DirectionalLight, Vec3, TextNode, Filename, getModelPath
from direct.gui.DirectGui import DirectButton
import time, random, math, os
from direct.gui.OnscreenText import OnscreenText

#In deze code staan het gebruik van functies en hun definities ver uit elkaar. Dit is vanwege de self-conventie.
#Deze conventie zorgt ervoor dat bepaalde definities overal in de code aangeroepen kunnen worden. Teun gebruikt "self" niet zoveel als ik (Fin).

#In deze functie is het gehele programma te vinden.
class RBMKv1(ShowBase):

    def __init__(self):
        super().__init__()

        #Een selectie lege lijsten, hier wordt later informatie in opgeslagen.
        self.neutronen = []
        self.neutronen_aanwezig = []
        self.neutronen_erbij = []
        self.neutronen_weg = []
        self.tijdstappen = []
        #Er worden de teksten voor de informatie in de scene aangemaakt. Deze staan links bovenin het scherm en worden constant geüpdatet.
        self.tekst_neutronen_aangemaakt = OnscreenText(text=f"Aantal neutronen aangemaakt: {str(len(self.neutronen))}", pos=(-1.3, 0.8), scale=0.07, fg=(0, 0, 0, 1), align=TextNode.ALeft)
        self.tekst_neutronen_aanwezig = OnscreenText(text=f"Aantal neutronen aanwezig: {str(len(self.neutronen_aanwezig))}", pos=(-1.3, 0.7), scale=0.07, fg=(0, 0, 0, 1), align=TextNode.ALeft)
        self.tekst_K = OnscreenText(text=f"K = 0.0", pos=(-1.3, 0.6), scale=0.07, fg=(0, 0, 0, 1), align=TextNode.ALeft)
        self.tekst_t = OnscreenText(text=f"Tijdstap {(len(self.tijdstappen))}", pos=(-1.3, 0.5), scale=0.07, fg=(0, 0, 0, 1), align=TextNode.ALeft)
        self.tekst_status = OnscreenText(text=f"De reactie is niet opgestart.", pos=(-1.3, 0.4), scale=0.07, fg=(0, 0, 0, 1), align=TextNode.ALeft)

        #De camera word ingesteld.
        self.enableMouse()
        #De ingebouwde muisbesturing van Panda3D wordt ingeschakeld. De camera kan alleen handmatig worden bestuurd.
        # Met de rechtermuisknop kan de camera bewegen.
        # Door het indrukken van het scrollwheel kan de camera draaien.
        # Met de linkermuisknop kan de camera in- en uitzoomen.

        #Er wordt licht toegevoegd aan de scene.
        alight = AmbientLight('alight')
        alight.setColor((0.5, 0.5, 0.5, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)

        dlight = DirectionalLight('dlight')
        dlight.setColor((1, 1, 1, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(45, -30, 0)
        self.render.setLight(dlnp)

        #De kernen worden op volgorde van links naar rechts stuk voor stuk aangemaakt.
        #De definitie van de kern_laag functie is te vinden op regel 000. Dit is zodat de functie overal in de code gebruikt kan worden.

        #kolom -4
        kernAx_4y2, kernBx_4y2, kernCx_4y2, kernDx_4y2, kernEx_4y2 = self.kern_laag(-32, 16)
        kernAx_4y1, kernBx_4y1, kernCx_4y1, kernDx_4y1, kernEx_4y1 = self.kern_laag(-32, 8)
        kernAx_4y_1, kernBx_4y_1, kernCx_4y_1, kernDx_4y_1, kernEx_4y_1 = self.kern_laag(-32, -8)
        kernAx_4y_2, kernBx_4y_2, kernCx_4y_2, kernDx_4y_2, kernEx_4y_2 = self.kern_laag(-32, -16)
        #kolom -3
        kernAx_3y3, kernBx_3y3, kernCx_3y3, kernDx_3y3, kernEx_3y3 = self.kern_laag(-24, 24)
        kernAx_3y2, kernBx_3y2, kernCx_3y2, kernDx_3y2, kernEx_3y2 = self.kern_laag(-24, 16)
        kernAx_3y1, kernBx_3y1, kernCx_3y1, kernDx_3y1, kernEx_3y1 = self.kern_laag(-24, 8)
        kernAx_3y0, kernBx_3y0, kernCx_3y0, kernDx_3y0, kernEx_3y0 = self.kern_laag(-24, 0)
        kernAx_3y_1, kernBx_3y_1, kernCx_3y_1, kernDx_3y_1, kernEx_3y_1 = self.kern_laag(-24, -8)
        kernAx_3y_2, kernBx_3y_2, kernCx_3y_2, kernDx_3y_2, kernEx_3y_2 = self.kern_laag(-24, -16)
        kernAx_3y_3, kernBx_3y_3, kernCx_3y_3, kernDx_3y_3, kernEx_3y_3 = self.kern_laag(-24, -24)
        #kolom -2
        kernAx_2y4, kernBx_2y4, kernCx_2y4, kernDx_2y4, kernEx_2y4 = self.kern_laag(-16, 32)
        kernAx_2y3, kernBx_2y3, kernCx_2y3, kernDx_2y3, kernEx_2y3 = self.kern_laag(-16, 24)
        kernAx_2y1, kernBx_2y1, kernCx_2y1, kernDx_2y1, kernEx_2y1 = self.kern_laag(-16, 8)
        kernAx_2y0, kernBx_2y0, kernCx_2y0, kernDx_2y0, kernEx_2y0 = self.kern_laag(-16, 0)
        kernAx_2y_1, kernBx_2y_1, kernCx_2y_1, kernDx_2y_1, kernEx_2y_1 = self.kern_laag(-16, -8)
        kernAx_2y_3, kernBx_2y_3, kernCx_2y_3, kernDx_2y_3, kernEx_2y_3 = self.kern_laag(-16, -24)
        kernAx_2y_4, kernBx_2y_4, kernCx_2y_4, kernDx_2y_4, kernEx_2y_4 = self.kern_laag(-16, -32)
        #kolom -1
        kernAx_1y4, kernBx_1y4, kernCx_1y4, kernDx_1y4, kernEx_1y4 = self.kern_laag(-8, 32)
        kernAx_1y3, kernBx_1y3, kernCx_1y3, kernDx_1y3, kernEx_1y3 = self.kern_laag(-8, 24)
        kernAx_1y2, kernBx_1y2, kernCx_1y2, kernDx_1y2, kernEx_1y2 = self.kern_laag(-8, 16)
        kernAx_1y1, kernBx_1y1, kernCx_1y1, kernDx_1y1, kernEx_1y1 = self.kern_laag(-8, 8)
        kernAx_1y0, kernBx_1y0, kernCx_1y0, kernDx_1y0, kernEx_1y0 = self.kern_laag(-8, 0)
        kernAx_1y_1, kernBx_1y_1, kernCx_1y_1, kernDx_1y_1, kernEx_1y_1 = self.kern_laag(-8, -8)
        kernAx_1y_2, kernBx_1y_2, kernCx_1y_2, kernDx_1y_2, kernEx_1y_2 = self.kern_laag(-8, -16)
        kernAx_1y_3, kernBx_1y_3, kernCx_1y_3, kernDx_1y_3, kernEx_1y_3 = self.kern_laag(-8, -24)
        kernAx_1y_4, kernBx_1y_4, kernCx_1y_4, kernDx_1y_4, kernEx_1y_4 = self.kern_laag(-8, -32)
        #kolom 0
        kernAx0y3, kernBx0y3, kernCx0y3, kernDx0y3, kernEx0y3 = self.kern_laag(0, 24)
        kernAx0y2, kernBx0y2, kernCx0y2, kernDx0y2, kernEx0y2 = self.kern_laag(0, 16)
        kernAx0y1, kernBx0y1, kernCx0y1, kernDx0y1, kernEx0y1 = self.kern_laag(0, 8)
        kernAx0y_1, kernBx0y_1, kernCx0y_1, kernDx0y_1, kernEx0y_1 = self.kern_laag(0, -8)
        kernAx0y_2, kernBx0y_2, kernCx0y_2, kernDx0y_2, kernEx0y_2 = self.kern_laag(0, -16)
        kernAx0y_3, kernBx0y_3, kernCx0y_3, kernDx0y_3, kernEx0y_3 = self.kern_laag(0, -24)
        #kolom 1
        kernAx1y4, kernBx1y4, kernCx1y4, kernDx1y4, kernEx1y4 = self.kern_laag(8, 32)
        kernAx1y3, kernBx1y3, kernCx1y3, kernDx1y3, kernEx1y3 = self.kern_laag(8, 24)
        kernAx1y2, kernBx1y2, kernCx1y2, kernDx1y2, kernEx1y2 = self.kern_laag(8, 16)
        kernAx1y1, kernBx1y1, kernCx1y1, kernDx1y1, kernEx1y1 = self.kern_laag(8, 8)
        kernAx1y0, kernBx1y0, kernCx1y0, kernDx1y0, kernEx1y0 = self.kern_laag(8, 0)
        kernAx1y_1, kernBx1y_1, kernCx1y_1, kernDx1y_1, kernEx1y_1 = self.kern_laag(8, -8)
        kernAx1y_2, kernBx1y_2, kernCx1y_2, kernDx1y_2, kernEx1y_2 = self.kern_laag(8, -16)
        kernAx1y_3, kernBx1y_3, kernCx1y_3, kernDx1y_3, kernEx1y_3 = self.kern_laag(8, -24)
        kernAx1y_4, kernBx1y_4, kernCx1y_4, kernDx1y_4, kernEx1y_4 = self.kern_laag(8, -32)
        #kolom 2
        kernAx2y4, kernBx2y4, kernCx2y4, kernDx2y4, kernEx2y4 = self.kern_laag(16, 32)
        kernAx2y3, kernBx2y3, kernCx2y3, kernDx2y3, kernEx2y3 = self.kern_laag(16, 24)
        kernAx2y1, kernBx2y1, kernCx2y1, kernDx2y1, kernEx2y1 = self.kern_laag(16, 8)
        kernAx2y0, kernBx2y0, kernCx2y0, kernDx2y0, kernEx2y0 = self.kern_laag(16, 0)
        kernAx2y_1, kernBx2y_1, kernCx2y_1, kernDx2y_1, kernEx2y_1 = self.kern_laag(16, -8)
        kernAx2y_3, kernBx2y_3, kernCx2y_3, kernDx2y_3, kernEx2y_3 = self.kern_laag(16, -24)
        kernAx2y_4, kernBx2y_4, kernCx2y_4, kernDx2y_4, kernEx2y_4 = self.kern_laag(16, -32)
        # Kolom 3
        kernAx3y3, kernBx3y3, kernCx3y3, kernDx3y3, kernEx3y3 = self.kern_laag(24, 24)
        kernAx3y2, kernBx3y2, kernCx3y2, kernDx3y2, kernEx3y2 = self.kern_laag(24, 16)
        kernAx3y1, kernBx3y1, kernCx3y1, kernDx3y1, kernEx3y1 = self.kern_laag(24, 8)
        kernAx3y0, kernBx3y0, kernCx3y0, kernDx3y0, kernEx3y0 = self.kern_laag(24, 0)
        kernAx3y_1, kernBx3y_1, kernCx3y_1, kernDx3y_1, kernEx3y_1 = self.kern_laag(24, -8)
        kernAx3y_2, kernBx3y_2, kernCx3y_2, kernDx3y_2, kernEx3y_2 = self.kern_laag(24, -16)
        kernAx3y_3, kernBx3y_3, kernCx3y_3, kernDx3y_3, kernEx3y_3 = self.kern_laag(24, -24)
        # Kolom 4
        kernAx4y2, kernBx4y2, kernCx4y2, kernDx4y2, kernEx4y2 = self.kern_laag(32, 16)
        kernAx4y1, kernBx4y1, kernCx4y1, kernDx4y1, kernEx4y1 = self.kern_laag(32, 8)
        kernAx4y_1, kernBx4y_1, kernCx4y_1, kernDx4y_1, kernEx4y_1 = self.kern_laag(32, -8)
        kernAx4y_2, kernBx4y_2, kernCx4y_2, kernDx4y_2, kernEx4y_2 = self.kern_laag(32, -16)

        #Er wordt een lijst aangemaakt met elke kern in de reactor, deze bevat dus zowel U-235 kernen als kernen van splijtingsproducten.
        self.kernen = [
            #EERSTE SCHIL: RADIUS 4
            kernAx_4y2, kernBx_4y2, kernCx_4y2, kernDx_4y2, kernEx_4y2,
            kernAx_4y1, kernBx_4y1, kernCx_4y1, kernDx_4y1, kernEx_4y1,
            kernAx_4y_1, kernBx_4y_1, kernCx_4y_1, kernDx_4y_1, kernEx_4y_1,
            kernAx_4y_2, kernBx_4y_2, kernCx_4y_2, kernDx_4y_2, kernEx_4y_2,
            kernAx_3y3, kernBx_3y3, kernCx_3y3, kernDx_3y3, kernEx_3y3,
            kernAx_3y2, kernBx_3y2, kernCx_3y2, kernDx_3y2, kernEx_3y2,
            kernAx_3y1, kernBx_3y1, kernCx_3y1, kernDx_3y1, kernEx_3y1,
            kernAx_3y0, kernBx_3y0, kernCx_3y0, kernDx_3y0, kernEx_3y0,
            kernAx_3y_1, kernBx_3y_1, kernCx_3y_1, kernDx_3y_1, kernEx_3y_1,
            kernAx_3y_2, kernBx_3y_2, kernCx_3y_2, kernDx_3y_2, kernEx_3y_2,
            kernAx_3y_3, kernBx_3y_3, kernCx_3y_3, kernDx_3y_3, kernEx_3y_3,
            kernAx_2y4, kernBx_2y4, kernCx_2y4, kernDx_2y4, kernEx_2y4,
            kernAx_2y3, kernBx_2y3, kernCx_2y3, kernDx_2y3, kernEx_2y3,
            kernAx_2y1, kernBx_2y1, kernCx_2y1, kernDx_2y1, kernEx_2y1,
            kernAx_2y0, kernBx_2y0, kernCx_2y0, kernDx_2y0, kernEx_2y0,
            kernAx_2y_1, kernBx_2y_1, kernCx_2y_1, kernDx_2y_1, kernEx_2y_1,
            kernAx_2y_3, kernBx_2y_3, kernCx_2y_3, kernDx_2y_3, kernEx_2y_3,
            kernAx_2y_4, kernBx_2y_4, kernCx_2y_4, kernDx_2y_4, kernEx_2y_4,
            kernAx_1y4, kernBx_1y4, kernCx_1y4, kernDx_1y4, kernEx_1y4,
            kernAx_1y3, kernBx_1y3, kernCx_1y3, kernDx_1y3, kernEx_1y3,
            kernAx_1y2, kernBx_1y2, kernCx_1y2, kernDx_1y2, kernEx_1y2,
            kernAx_1y1, kernBx_1y1, kernCx_1y1, kernDx_1y1, kernEx_1y1,
            kernAx_1y0, kernBx_1y0, kernCx_1y0, kernDx_1y0, kernEx_1y0,
            kernAx_1y_1, kernBx_1y_1, kernCx_1y_1, kernDx_1y_1, kernEx_1y_1,
            kernAx_1y_2, kernBx_1y_2, kernCx_1y_2, kernDx_1y_2, kernEx_1y_2,
            kernAx_1y_3, kernBx_1y_3, kernCx_1y_3, kernDx_1y_3, kernEx_1y_3,
            kernAx_1y_4, kernBx_1y_4, kernCx_1y_4, kernDx_1y_4, kernEx_1y_4,
            kernAx0y3, kernBx0y3, kernCx0y3, kernDx0y3, kernEx0y3,
            kernAx0y2, kernBx0y2, kernCx0y2, kernDx0y2, kernEx0y2,
            kernAx0y1, kernBx0y1, kernCx0y1, kernDx0y1, kernEx0y1,
            kernAx0y_1, kernBx0y_1, kernCx0y_1, kernDx0y_1, kernEx0y_1,
            kernAx0y_2, kernBx0y_2, kernCx0y_2, kernDx0y_2, kernEx0y_2,
            kernAx0y_3, kernBx0y_3, kernCx0y_3, kernDx0y_3, kernEx0y_3,
            kernAx1y4, kernBx1y4, kernCx1y4, kernDx1y4, kernEx1y4,
            kernAx1y3, kernBx1y3, kernCx1y3, kernDx1y3, kernEx1y3,
            kernAx1y2, kernBx1y2, kernCx1y2, kernDx1y2, kernEx1y2,
            kernAx1y1, kernBx1y1, kernCx1y1, kernDx1y1, kernEx1y1,
            kernAx1y0, kernBx1y0, kernCx1y0, kernDx1y0, kernEx1y0,
            kernAx1y_1, kernBx1y_1, kernCx1y_1, kernDx1y_1, kernEx1y_1,
            kernAx1y_2, kernBx1y_2, kernCx1y_2, kernDx1y_2, kernEx1y_2,
            kernAx1y_3, kernBx1y_3, kernCx1y_3, kernDx1y_3, kernEx1y_3,
            kernAx1y_4, kernBx1y_4, kernCx1y_4, kernDx1y_4, kernEx1y_4,
            kernAx2y4, kernBx2y4, kernCx2y4, kernDx2y4, kernEx2y4,
            kernAx2y3, kernBx2y3, kernCx2y3, kernDx2y3, kernEx2y3,
            kernAx2y1, kernBx2y1, kernCx2y1, kernDx2y1, kernEx2y1,
            kernAx2y0, kernBx2y0, kernCx2y0, kernDx2y0, kernEx2y0,
            kernAx2y_1, kernBx2y_1, kernCx2y_1, kernDx2y_1, kernEx2y_1,
            kernAx2y_3, kernBx2y_3, kernCx2y_3, kernDx2y_3, kernEx2y_3,
            kernAx2y_4, kernBx2y_4, kernCx2y_4, kernDx2y_4, kernEx2y_4,
            kernAx3y3, kernBx3y3, kernCx3y3, kernDx3y3, kernEx3y3,
            kernAx3y2, kernBx3y2, kernCx3y2, kernDx3y2, kernEx3y2,
            kernAx3y1, kernBx3y1, kernCx3y1, kernDx3y1, kernEx3y1,
            kernAx3y0, kernBx3y0, kernCx3y0, kernDx3y0, kernEx3y0,
            kernAx3y_1, kernBx3y_1, kernCx3y_1, kernDx3y_1, kernEx3y_1,
            kernAx3y_2, kernBx3y_2, kernCx3y_2, kernDx3y_2, kernEx3y_2,
            kernAx3y_3, kernBx3y_3, kernCx3y_3, kernDx3y_3, kernEx3y_3,
            kernAx4y2, kernBx4y2, kernCx4y2, kernDx4y2, kernEx4y2,
            kernAx4y1, kernBx4y1, kernCx4y1, kernDx4y1, kernEx4y1,
            kernAx4y_1, kernBx4y_1, kernCx4y_1, kernDx4y_1, kernEx4y_1,
            kernAx4y_2, kernBx4y_2, kernCx4y_2, kernDx4y_2, kernEx4y_2
        ]
        #Aan deze lijsten worden later kernen toegevoegd.
        #De U_kernen zijn U-235 kernen.
        self.U_kernen = []
        #De extra_kernen zijn kernen die later aan de reactor worden toegevoegd, als de absorptie is uitgeschakeld.
        self.extra_kernen = []

        #De telling van de tijdstappen wordt gestart. Elke tijstap is 3 seconden. 
        #De definitie van de tijd_taak functie is te vinden op regel 000.
        self.tijd_taak(self.kernen, Task)
        self.taskMgr.doMethodLater(3, self.tijd_taak, "TijdTaak", extraArgs=[self.kernen], appendTask=True)

        #De absorptie staven worden aangemaakt. Deze representeren alles wat de kernsplijting kan stoppen (regelstaven, koelwater, Xenon, etc).
        #De definitie van de staaf_afstand functie is te vinden op regel 000.

        staafx0y0 = self.staaf(0, 0)
        staafx4y0 = self.staaf(32, 0)
        staafx_4y0 = self.staaf(-32, 0)
        staafx0y4 = self.staaf(0, 32)
        staafx0y_4 = self.staaf(0, -32)
        staafx2y2 = self.staaf(16, 16)
        staafx_2y2 = self.staaf(-16, 16)
        staafx2y_2 = self.staaf(16, -16)
        staafx_2y_2 = self.staaf(-16, -16)
        self.staven = [staafx0y0, staafx4y0, staafx_4y0, staafx0y4, staafx0y_4, staafx2y2, staafx_2y2, staafx2y_2, staafx_2y_2]

        #De knoppen worden aangemaakt. Deze knoppen zijn te vinden in de scene en kunnen worden aangeklikt.
        #Deze knop zorgt ervoor dat de start_reactie functie wordt uitgevoerd. Deze functie zorgt ervoor dat vier willekeurige kernen kernsplijting ondergaan.
        #De definitie van de start_reactie functie is te vinden op regel 000.
        self.start_knop = DirectButton(text="start", scale=0.125, command=lambda: self.start_reactie())
        self.start_knop.setPos(-0.75, 0, -0.75)
        #Deze knop zorgt ervoor dat de activeer_deactiveer_absorptie functie wordt uitgevoerd. Deze functie zorgt ervoor dat de absorptie staven worden verschijnen of verdwijnen.
        #De definitie van de activeer_deactiveer_absorptie functie is te vinden op regel 000.
        self.absorptie_knop = DirectButton(text="(de)activeer absorptie", scale=0.125, command=lambda: self.activeer_deactiveer_absorptie())
        self.absorptie_knop.setPos(-0.75, 0, -0.95)

    #De functie neutron_taak uitvoeren meet de tijd en positie van een neutron voordat die gaat bewegen, en zorgt ervoor dat de neutron_taak functie elk frame wordt uitgevoerd.
    def neutron_taak_uitvoeren(self, neutron, U_kernen_kopie, staven_kopie, doel, taak_naam):
        nvector = neutron.getPos()
        t0 = time.time()
        self.taskMgr.add(self.neutron_taak, taak_naam, extraArgs=[neutron, U_kernen_kopie, staven_kopie, doel, nvector, t0, taak_naam], appendTask=True)

    #De functie neutron_taak  berekent elk frame de nieuwe positie van een neutron en past deze toe. 
    #Ook controleert hij per frame of de neutron een botsing heeft met een U-235 kern of absorptie staaf, en of hij de scene heeft verlaten.
    #Verder berekent hij de nieuwe waardes van de tekst op het scherm, en past deze toe.
    def neutron_taak(self, neutron, U_kernen_kopie, staven_kopie, doel, nvector, t0, taak_naam, task):
        #Een neutron beweegt richting een doel, die aan hem is toegewezen. Dit kan een U-235 kern, absorptie staaf of een willekeurige positie zijn.
        #Een neutron bereikt zijn toegewezen kern niet altijd, omdat er bijvoorbeeld een absorptie staaf tussen hem en zijn doel kan staan.
        if doel == "splijting":
            #Het verschil in tijd sinds het begin van de taak wordt berekend.
            t = time.time()
            dt = t - t0
            #Als de neutron nog geen kern als doel heeft, krijgt hij hiervoor een willekeurige U-235 kern toegewezen.
            #Omdat de lijst self.U_kernen kan veranderen, wordt er een kopie van de lijst gebruikt.
            if not hasattr(task, "doelkern"):
                task.doelkern = random.choice(U_kernen_kopie).getPos()
            #De positie van het doel wordt bepaald.
            Uvector = task.doelkern
            #Met vectoren wordt de positie van de neutron berekend. Zie voor verdere uitleg van de wiskunde het verslag.
            Lengte = math.sqrt((Uvector[0] - nvector[0])**2 + (Uvector[1] - nvector[1])**2 + (Uvector[2] - nvector[2])**2)
            if Lengte == 0:
                Lengte = 0.0001
            xn = nvector[0] + 3 * dt * ((Uvector[0] - nvector[0]) / Lengte)
            yn = nvector[1] + 3 * dt * ((Uvector[1] - nvector[1]) / Lengte)
            zn = nvector[2] + 3 * dt * ((Uvector[2] - nvector[2]) / Lengte)
            neutron.setPos(xn, yn, zn)
        #Hier beweegt de neutron naar een absorptie staaf, die hem kan absorberen.
        elif doel == "absorptie":
            t = time.time()
            dt = t - t0
            if not hasattr(task, "doelstaaf"):
                task.doelstaaf = random.choice(staven_kopie).getPos()
            Avector = task.doelstaaf
            Lengte = math.sqrt((Avector[0] - nvector[0])**2 + (Avector[1] - nvector[1])**2 + (Avector[2] - nvector[2])**2)
            if Lengte == 0:
                Lengte = 0.0001
            xn = nvector[0] + 3 * dt * ((Avector[0] - nvector[0]) / Lengte)
            yn = nvector[1] + 3 * dt * ((Avector[1] - nvector[1]) / Lengte)
            zn = nvector[2] + 3 * dt * ((Avector[2] - nvector[2]) / Lengte)
            neutron.setPos(xn, yn, zn)
        #Hier beweegt de neutron richting een willekeurige positie in de reactor.
        elif doel == "random":
            t = time.time()
            dt = t - t0
            if not hasattr(task, "doelrandom"):
                task.doelrandom = (random.randint(-32, 32), random.randint(-32, 32), random.randint(-16, 16))
            randomvector = task.doelrandom
            Lengte = math.sqrt((randomvector[0] - nvector[0])**2 + (randomvector[1] - nvector[1])**2 + (randomvector[2] - nvector[2])**2)
            xn = nvector[0] + 3 * dt * ((randomvector[0] - nvector[0]) / Lengte)
            yn = nvector[1] + 3 * dt * ((randomvector[1] - nvector[1]) / Lengte)
            zn = nvector[2] + 3 * dt * ((randomvector[2] - nvector[2]) / Lengte)
            if Lengte == 0:
                Lengte = 0.0001
            neutron.setPos(xn, yn, zn)

        #Er wort gecontroleerd of de neutron dichtbij genoeg is bij een U-235 kern om een botsing te veroorzaken.
        for U_kern in self.U_kernen:
            try:
                #Als de afstand tussen de neutron en de U-235 kern kleiner is dan 2, dan vindt de kernsplijting plaats.
                if math.isclose(U_kern.getX(), neutron.getX(), abs_tol = 2) and\
                math.isclose(U_kern.getY(), neutron.getY(), abs_tol = 2) and\
                math.isclose(U_kern.getZ(), neutron.getZ(), abs_tol = 2):
                    #Omdat elke kern hetzelfde model heeft, geeft Panda3D ze allemaal dezelfde naam in de U_kernen lijst.
                    #Daarom wordt de index van de kern in de lijst gezocht en gebruikt, zodat de juiste kern alsnog kan worden verwijderd.
                    #De kern representeert na de splijting tenslotte geen U-235 kern meer, maar een splijtingsproduct.
                    index = self.U_kernen.index(U_kern)
                    self.U_kernen.remove(self.U_kernen[index])
                    #Debug
                    print(self.U_kernen)
                    print(f"Neutron met taak {taak_naam} heeft gebotst met Uraniumkern op {U_kern.getPos()}.")
                    #Einde debug
                    #De neutron wordt verwijderd en haar taak wordt gestopt.
                    self.taskMgr.remove(taak_naam)
                    neutron.removeNode()
                    neutron = None
                    #Lijsten worden bijgewerkt
                    if self.neutronen_aanwezig:
                        self.neutronen_aanwezig.pop()
                    self.neutronen_weg.append(1)
                    self.taskMgr.doMethodLater(3, self.aantallen_neutronen_reset, "ResetNeutronenWaardesTaak", extraArgs=[self.neutronen_weg], appendTask=True)
                    #Kernsplijting vindt plaats met de kernspltijing functie. De definitie van deze functie is te vinden op regel 000.
                    self.kernsplijting(U_kern)
                    return Task.done
            #In zeer zeldzame gevallen probeert de code een U-235 kern te vinden die niet meer bestaat, als deze op hetzelfde moment is verwijderd.
            #In een dergelijk geval verschijnt er een foutmelding in de console, maar het programma wordt niet stopgezet.
            except Exception as e:
                print(f"De code probeerde een Uraniumkern de vinden, dit niet meer bestaat. Foutmelding: {e}")

    #Er wordt gecontroleerd of de neutron dichtbij genoeg is bij een absorptie staaf om te worden geabsorbeerd, op dezelfde manier als bij de U-235 kernen.
        for staaf in self.staven:
            try:
                if math.isclose(staaf.getX(), neutron.getX(), abs_tol = 3) and\
                math.isclose(staaf.getY(), neutron.getY(), abs_tol = 3) and\
                math.isclose(staaf.getZ(), neutron.getZ(), abs_tol = 25):
                    print(f"Neutron met taak {taak_naam} geabsorbeerd door staaf op {staaf.getPos()}.")
                    self.taskMgr.remove(taak_naam)
                    neutron.removeNode()
                    neutron = None
                    if self.neutronen_aanwezig:
                        self.neutronen_aanwezig.pop()
                    self.neutronen_weg.append(1)
                    self.taskMgr.doMethodLater(3, self.aantallen_neutronen_reset, "ResetNeutronenWaardesTaak", extraArgs=[self.neutronen_weg], appendTask=True)
                    return Task.done
            except Exception as e:
                print(f"De code probeerde een staaf te vinden, die niet meer bestaat. Foutmelding: {e}")

        #Er wordt gecontroleerd of de neutron de scène heeft verlaten, hierbij is geen failsafe nodig.
        if neutron.getX() < -40 or neutron.getX() > 40 or\
           neutron.getY() < -40 or neutron.getY() > 40 or\
           neutron.getZ() < -40 or neutron.getZ() > 40:
            print(f"Neutron met taak {taak_naam} heeft de scène verlaten.")
            self.taskMgr.remove(taak_naam)
            neutron.removeNode()
            neutron = None
            if self.neutronen_aanwezig:
                self.neutronen_aanwezig.pop()
            self.neutronen_weg.append(1)
            self.taskMgr.doMethodLater(3, self.aantallen_neutronen_reset, "ResetNeutronenWaardesTaak", extraArgs=[self.neutronen_weg], appendTask=True)
            return Task.done

        #De teksten links bovenin het scherm worden bijgewerkt.
        self.tekst_neutronen_aanwezig.setText(f"Aantal neutronen aanwezig: {len(self.neutronen_aanwezig)}")
        self.tekst_neutronen_aangemaakt.setText(f"Aantal neutronen aangemaakt: {len(self.neutronen)}")
        if len(self.neutronen_weg) == 0:
            K = 0
        else:
            K = (len(self.neutronen_erbij) + 1) / len(self.neutronen_weg)
        #Voor de relevantie van de waarde K, zie het verslag.
        self.tekst_K.setText(f"K = {K}")
        if K > 1:
            self.tekst_status.setText("De reactie is superkritisch.")
        elif K == 1:
            self.tekst_status.setText("De reactie is kritisch.")
        elif K < 1:
            self.tekst_status.setText("De reactie is subkritisch.")
        print(str(taak_naam))
        return Task.cont

    #De functie kernsplijting zorgt voor drie nieuwe neutronen met willekeurige doelen, en maakt van de geraakte U-235 kern een splijtingsproduct.
    def kernsplijting(self, U_kern):
        #De kern wordt rood.
        U_kern.setColor(1, 0, 0, 1)
        #Als de U-235 kern in de U_kernen lijst zit, wordt deze verwijderd.
        if U_kern in self.U_kernen:
            index = self.U_kernen.index(U_kern)        
            self.U_kernen.remove(self.U_kernen[index])
        #Het volgende stukje code wordt driemaal uitgevoerd.
        for i in range(3):
            if self.staven:
                doelen = ["splijting", "splijting", "splijting", "splijting", "absorptie", "random", "random"]
            else:
                doelen = ["splijting", "splijting", "splijting", "splijting", "splijting", "random", "random"]
            doel = random.choice(doelen)
            print(f"Doel neutron: {doel}")
            neutron = self.loader.loadModel("my-models/testgeodetie.egg")
            neutron.reparentTo(self.render)
            neutron.setScale(1)
            neutron.setHpr(0, 0, 0)
            neutron.setPos(U_kern.getX(), U_kern.getY(), U_kern.getZ())
            neutron.setColor(0, 1, 0, 1)
            #De lijsten worden bijgewerkt.
            self.neutronen.append(1)
            self.neutronen_aanwezig.append(1)
            self.neutronen_erbij.append(1)
            self.taskMgr.doMethodLater(3, self.aantallen_neutronen_reset, "ResetNeutronenWaardesTaak", extraArgs=[self.neutronen_erbij], appendTask=True)
            #Debug
            print(f"Neutron {len(self.neutronen)} is aangemaakt op {neutron.getPos()}")
            #Einde debug
            #De neutron wordt constant geüpdatet met de neutron_taak functie.
            #De definitie van deze functie is te vinden op regel 000.
            self.neutron_taak_uitvoeren(neutron, self.U_kernen.copy(), self.staven.copy(), doel, f"NeutronTaak_{len(self.neutronen)}")
        #De kleur van de kern wordt na drie seconden teruggezet naar wit met de kern_kleur_reset functie.
        #De definitie van deze functie is te vinden op regel 000.
        self.taskMgr.doMethodLater(2, self.kern_kleur_reset, "KernKleurResetTaak", extraArgs=[U_kern], appendTask=True)

    def staaf(self, x, y):
        staaf = self.loader.loadModel("my-models/RegelstaafBeta.egg")
        staaf.reparentTo(self.render)
        staaf.setScale(4)
        staaf.setHpr(0, 0, 0)
        staaf.setPos(x, y, 0)
        return staaf

    def kern_laag(self,x,y):
        kernA = self.loader.loadModel("my-models/testbol.egg")
        kernA.reparentTo(self.render)
        kernA.setScale(2.5)
        kernA.setHpr(0, 0, 0)
        kernA.setPos(x, y, 16)
        kernA.setColor(1, 1, 1, 1)
        kernB = self.loader.loadModel("my-models/testbol.egg")
        kernB.reparentTo(self.render)
        kernB.setScale(2.5)
        kernB.setHpr(0, 0, 0)
        kernB.setPos(x, y, 8)
        kernB.setColor(1, 1, 1, 1)
        kernC = self.loader.loadModel("my-models/testbol.egg")
        kernC.reparentTo(self.render)
        kernC.setScale(2.5)
        kernC.setHpr(0, 0, 0)
        kernC.setPos(x, y, 0)
        kernC.setColor(1, 1, 1, 1)
        kernD = self.loader.loadModel("my-models/testbol.egg")
        kernD.reparentTo(self.render)
        kernD.setScale(2.5)
        kernD.setHpr(0, 0, 0)
        kernD.setColor(1, 1, 1, 1)
        kernD.setPos(x, y, -8)
        kernE = self.loader.loadModel("my-models/testbol.egg")
        kernE.reparentTo(self.render)
        kernE.setScale(2.5)
        kernE.setHpr(0, 0, 0)
        kernE.setPos(x, y, -16)
        kernE.setColor(1, 1, 1, 1)
        return kernA, kernB, kernC, kernD, kernE

    def activeer_deactiveer_absorptie(self):
        if self.staven:
            for staaf in self.staven:
                staaf.removeNode()
                staaf = None
            self.staven.clear()

            kernAx0y0, kernBx0y0, kernCx0y0, kernDx0y0, kernEx0y0 = self.kern_laag(0, 0)
            kernAx4y0, kernBx4y0, kernCx4y0, kernDx4y0, kernEx4y0 = self.kern_laag(32, 0)
            kernAx_4y0, kernBx_4y0, kernCx_4y0, kernDx_4y0, kernEx_4y0 = self.kern_laag(-32, 0)
            kernAx0y4, kernBx0y4, kernCx0y4, kernDx0y4, kernEx0y4 = self.kern_laag(0, 32)
            kernAx0y_4, kernBx0y_4, kernCx0y_4, kernDx0y_4, kernEx0y_4 = self.kern_laag(0, -32)
            kernAx2y2, kernBx2y2, kernCx2y2, kernDx2y2, kernEx2y2 = self.kern_laag(16, 16)
            kernAx_2y2, kernBx_2y2, kernCx_2y2, kernDx_2y2, kernEx_2y2 = self.kern_laag(-16, 16)
            kernAx2y_2, kernBx2y_2, kernCx2y_2, kernDx2y_2, kernEx2y_2 = self.kern_laag(16, -16)
            kernAx_2y_2, kernBx_2y_2, kernCx_2y_2, kernDx_2y_2, kernEx_2y_2 = self.kern_laag(-16, -16)
            self.kernen.extend([
                kernAx0y0, kernBx0y0, kernCx0y0, kernDx0y0, kernEx0y0,
                kernAx4y0, kernBx4y0, kernCx4y0, kernDx4y0, kernEx4y0,
                kernAx_4y0, kernBx_4y0, kernCx_4y0, kernDx_4y0, kernEx_4y0,
                kernAx0y4, kernBx0y4, kernCx0y4, kernDx0y4, kernEx0y4,
                kernAx0y_4, kernBx0y_4, kernCx0y_4, kernDx0y_4, kernEx0y_4,
                kernAx2y2, kernBx2y2, kernCx2y2, kernDx2y2, kernEx2y2,
                kernAx_2y2, kernBx_2y2, kernCx_2y2, kernDx_2y2, kernEx_2y2,
                kernAx2y_2, kernBx2y_2, kernCx2y_2, kernDx2y_2, kernEx2y_2,
                kernAx_2y_2, kernBx_2y_2, kernCx_2y_2, kernDx_2y_2, kernEx_2y_2
            ])
            self.extra_kernen.extend([
                kernAx0y0, kernBx0y0, kernCx0y0, kernDx0y0, kernEx0y0,
                kernAx4y0, kernBx4y0, kernCx4y0, kernDx4y0, kernEx4y0,
                kernAx_4y0, kernBx_4y0, kernCx_4y0, kernDx_4y0, kernEx_4y0,
                kernAx0y4, kernBx0y4, kernCx0y4, kernDx0y4, kernEx0y4,
                kernAx0y_4, kernBx0y_4, kernCx0y_4, kernDx0y_4, kernEx0y_4,
                kernAx2y2, kernBx2y2, kernCx2y2, kernDx2y2, kernEx2y2,
                kernAx_2y2, kernBx_2y2, kernCx_2y2, kernDx_2y2, kernEx_2y2,
                kernAx2y_2, kernBx2y_2, kernCx2y_2, kernDx2y_2, kernEx2y_2,
                kernAx_2y_2, kernBx_2y_2, kernCx_2y_2, kernDx_2y_2, kernEx_2y_2
            ])

        else:
            for kern in self.extra_kernen:
                index = self.kernen.index(kern)
                self.kernen.remove(self.kernen[index])
                if kern in self.U_kernen:
                    index2 = self.U_kernen.index(kern)
                    self.U_kernen.remove(self.U_kernen[index2])
                kern.removeNode()
                kern = None
            self.extra_kernen.clear()
            staafx0y0 = self.staaf(0, 0)
            staafx4y0 = self.staaf(32, 0)
            staafx_4y0 = self.staaf(-32, 0)
            staafx0y4 = self.staaf(0, 32)
            staafx0y_4 = self.staaf(0, -32)
            staafx2y2 = self.staaf(16, 16)
            staafx_2y2 = self.staaf(-16, 16)
            staafx2y_2 = self.staaf(16, -16)
            staafx_2y_2 = self.staaf(-16, -16)
            self.staven = [staafx0y0, staafx4y0, staafx_4y0, staafx0y4, staafx0y_4, staafx2y2, staafx_2y2, staafx2y_2, staafx_2y_2]


    def kern_kleur_reset(self, U_kern, taak_naam):
        if U_kern and U_kern in self.U_kernen:
            U_kern.setColor(0, 1, 0, 1)
        elif U_kern and U_kern not in self.U_kernen:
            U_kern.setColor(1, 1, 1, 1)
        return Task.done

    def aantallen_neutronen_reset(self, lijst, Task):
        if len(lijst) > 0:
            lijst.pop()
        return Task.done

    def tijd_taak(self, kernen, task):
        self.tijdstappen.append(1)
        print(f"Tijdstap {len(self.tijdstappen)} gestart.")
        self.tekst_t.setText(f"Tijdstap {len(self.tijdstappen)}")
        if len(self.neutronen_aanwezig) == 0:
            self.tekst_neutronen_aanwezig.setText("Aantal neutronen aanwezig: 0")
            self.tekst_status.setText("De reactie is gestopt.")

        if len(self.U_kernen) < 7:
            for i in range(7 - len(self.U_kernen)):
                U_kern = random.choice(kernen)
                U_kern.setColor(0, 0, 1, 1)
                self.U_kernen.append(U_kern)
                print(f"Een radioactieve kern is op {U_kern.getPos()}")
        return task.again

    def start_reactie(self):
        for i in range(4):
            while True:
                kern = random.choice(self.kernen)
                if kern not in self.U_kernen:
                    break
            self.kernsplijting(kern)

programma = RBMKv1()
programma.run()