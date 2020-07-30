from flask import Flask, render_template, request, Response
import tempfile
from decimal import *

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')
    

@app.route('/gencode', methods=('GET', 'POST') )    
def gencode():  
    
    bedTemp	= 	request.form['bedTemp']
    dimensionX	= 	request.form['dimensionX']
    dimensionY	= 	request.form['dimensionY']
    extrusionMultiplier	= 	request.form['extrusionMultiplier']
    fanSpeed	= 	request.form['fanSpeed']
    fanSpeedIncrement	= 	request.form['fanSpeedIncrement']
    filamentDiameter	= 	request.form['filamentDiameter']
    incrementRetractiondistance	= 	request.form['incrementRetractiondistance']
    incrementRetractionspeed	= 	request.form['incrementRetractionspeed']
    layerHeight	= 	request.form['layerHeight']
    layersTest	= 	request.form['layersTest']
    nozzleDiameter	= 	request.form['nozzleDiameter']
    numTests	= 	request.form['numTests']
    printSpeed	= 	request.form['printSpeed']
    startRetractiondistance	= 	request.form['startRetractiondistance']
    startRetractionspeed	= 	request.form['startRetractionspeed']
    tempIncrementhotend	= 	request.form['tempIncrementhotend']
    tempStarthotend	= 	request.form['tempStarthotend']
    travelSpeed	= 	request.form['travelSpeed']
    customGcode	= 	request.form['customGcode']

    file = tempfile.TemporaryFile(mode='w+', encoding='utf-8')
    srd = float(startRetractiondistance)
    ird = float(incrementRetractiondistance)
        
    file.write(f';Calibration Generator 1.3.3\n')
    file.write(f";\n")
    file.write(f";\n")
    file.write(f";Retraction Distance from the top looking down\n")
    file.write(f";\n")
    file.write(f';       {round(Decimal(srd+ird*11),2)}    {round(Decimal(srd+ird*10),2)}    {round(Decimal(srd+ird*9),2)}    {round(Decimal(srd+ird*8),2)}\n')
    file.write(f";		|		|		|		|\n")
    file.write(f";\n")
    file.write(f";{round(Decimal(srd+ird*12),2)}-                               -{round(Decimal(srd+ird*7),2)}\n")
    file.write(f";\n")
    file.write(f";\n")
    file.write(f";{round(Decimal(srd+ird*13),2)}-                               -{round(Decimal(srd+ird*6),2)}\n")
    file.write(f";\n")
    file.write(f";\n")
    file.write(f";{round(Decimal(srd+ird*14),2)}-                               -{round(Decimal(srd+ird*5),2)}\n")
    file.write(f";\n")
    file.write(f";\n")
    file.write(f";{round(Decimal(srd+ird*15),2)}-                               -{round(Decimal(srd+ird*4),2)}\n")
    file.write(f";\n")
    file.write(f";		|		|		|		|\n")
    file.write(f";       {round(Decimal(srd+ird*0),2)}    {round(Decimal(srd+ird*1),2)}    {round(Decimal(srd+ird*2),2)}    {round(Decimal(srd+ird*3),2)}\n")
    file.write(f";\n")
    file.write(f";\n")
    
    srs = float(startRetractionspeed)
    irs = float(incrementRetractionspeed)
    tsh = float(tempStarthotend)
    tih = float(tempIncrementhotend)
    fs = float(fanSpeed)
    fsi = float(fanSpeedIncrement)
    lh = float(layerHeight)
    ts = float(travelSpeed)
    lt = float(layersTest)
    nt = float(numTests)


    file.write(f";Variables by Height\n")
    file.write(f";\n")
    file.write(f";Height         Retraction  Nozzle      Fan\n")
    file.write(f";               Speed       Temp        Speed\n")
    file.write(f";\n")

    cnt = int(nt-1)
    
    for loopx in range(int(nt)):
        file.write(f";{int(lt)} layers      {round(Decimal(srs+irs*cnt),2)}      {round(Decimal(tsh+tih*cnt),2)}      {round(Decimal(fs+fsi*cnt),2)}\n")
        cnt = cnt-1

    dx = float(dimensionX)
    dy = float(dimensionY)
    ps = float(printSpeed)
    nd = float(nozzleDiameter)
    fd = float(filamentDiameter)
    em = float(extrusionMultiplier)
    tb = float(bedTemp)    
    
    #Custom Gcode
    sgcode = str(customGcode)


    file.write(f";\n")
    file.write(f";\n")
    file.write(f";All inputs\n")
    file.write(f";\n")
    file.write(f";Dimension X 					{int(dx)}\n")
    file.write(f";Dimension Y 					{int(dy)}\n")
    file.write(f";Starting Retraction Distance	{srd}\n")
    file.write(f";Increment Retraction 			{ird}\n")
    file.write(f";Start Retraction Speed 		{srs}\n")
    file.write(f";Retraction Speed Increment 	{irs}\n")
    file.write(f";Print Speed 					{ps}\n")
    file.write(f";Starting Temp 					{int(tsh)}\n")
    file.write(f";Increment Temp 				{int(tih)}\n")
    file.write(f";Bed Temp 						{int(tb)}\n")
    file.write(f";Fan Speed 						{int(fs)}\n")
    file.write(f";Fan Speed Increment 			{int(fsi)}\n")
    file.write(f";Nozzle Diameter 				{nd}\n")
    file.write(f";Layer Height 					{lh}\n")
    file.write(f";Filament Diameter 				{fd}\n")
    file.write(f";Extrusion Multiplier 			{em}\n")
    file.write(f";Layers Per Test                {lt}\n")
    file.write(f";Number of Tests                {nt}\n")
    file.write(f";\n")
    file.write(f";\n")    
    

    # Generate E Value  https://3dprinting.stackexchange.com/questions/10171/how-is-e-value-calculated-in-slic3r 

    def eValue ( extrusionLength ):

        diameterNozzle = float(nozzleDiameter)
        heightLayer = float(layerHeight)
        diameterFilament = float(filamentDiameter)
        multiplierExtrusion = float(extrusionMultiplier)

        area = (diameterNozzle - heightLayer) * heightLayer + 3.14159 * (heightLayer/2)**2
        eValueresult = (area * extrusionLength * 4)/(3.14159 * diameterFilament**2/multiplierExtrusion)
        return eValueresult
    
    #start Gcode
    file.write(f";Start Gcode\n")
    file.write(f"M140 S{int(tb)}\n")
    file.write(f"M105\n")
    file.write(f"M190 S{int(tb)}\n")
    file.write(f"M104 S{int(tsh)}\n")
    file.write(f"M105\n")
    file.write(f"M109 S{int(tsh)}\n")
    file.write(f"M82\n")
    file.write(f"G28\n")
    file.write(f"G92 E0\n")
    file.write(f"G1 F200 E1\n")
    file.write(f"G92 E0\n")

    file.write(f"{sgcode}\n")

    file.write(f";\n")
    file.write(f";\n")

    xpos = dx/2-30
    ypos = dy/2-30
    zpos = lh
    epos = 0
    


    #Start Movement        
    file.write(f";Start Movement\n")
    file.write(f";\n")
    file.write(f"G1 Z2\n")
    file.write(f"G1 F{int(ts)*60} X{xpos} Y{ypos} Z{zpos}\n")
    file.write(f";\n")
    eValueresult = eValue(60)

    #Overextruding Raft
    evalueincrease = eValueresult*1.25
    eValueresult = evalueincrease


    remx = xpos
    remy = ypos

    file.write(f";Layer 1\n")

    #Horizontal

    for loopx in range(30):
        file.write(f"G1 F{int(ps*60/2)} X{xpos+60} Y{ypos} E{round(Decimal(eValueresult),5)}\n")
        xpos = xpos + 60
        eValueresult = eValueresult + evalueincrease
        file.write(f"G0 F{int(ts)*60} X{xpos} Y{ypos+1}\n")
        ypos = ypos + 1
        file.write(f"G1 F{int(ps*60/2)} X{xpos-60} Y{ypos} E{round(Decimal(eValueresult),5)}\n")
        xpos = xpos - 60
        eValueresult = eValueresult + evalueincrease
        file.write(f"G0 F{int(ts)*60} X{xpos} Y{ypos+1}\n")
        ypos = ypos + 1

    #Bring back to raft origin

    file.write(f"G0 F{int(ts)*60} X{xpos} Y{ypos} Z{round(Decimal(lh*3),2)}\n")
    file.write(f"G0 F{int(ts)*60} X{remx} Y{remy} Z{lh+lh}\n")
    xpos = remx
    ypos = remy

    file.write(f";Layer 2\n")

    #Vertical

    for loopx in range(30):
        file.write(f"G1 F{int(ps*60/2)} X{xpos} Y{ypos+60} E{round(Decimal(eValueresult),5)}\n")
        ypos = ypos + 60
        eValueresult = eValueresult + evalueincrease
        file.write(f"G0 F{int(ts)*60} X{xpos+1} Y{ypos}\n")
        xpos = xpos + 1
        file.write(f"G1 F{int(ps*60/2)} X{xpos} Y{ypos-60} E{round(Decimal(eValueresult),5)}\n")
        ypos = ypos - 60
        eValueresult = eValueresult + evalueincrease
        file.write(f"G0 F{int(ts)*60} X{xpos+1} Y{ypos}\n")
        xpos = xpos + 1    

    #Bring back to Calibration Starting Position

    file.write(f"G0 F{int(ts)*60} X{remx+5} Y{remy+5} Z{round(Decimal(lh*3),2)}\n")

    #Relative Movements

    file.write(f"M83\n")
    file.write(f"G91\n")

    #Start Calibration

    eValueresult = eValue(10)
    corenermarker = eValue(1)

    loopbigcount = 0
    loopsmallcount = 0

    layer = 3

    cnt = int(nt)
    lt = lt - 1

    for loopbig in range(int(cnt)):

    #set Fan every 15 layers
        file.write(f"M106 S{(round(Decimal((fs+fsi*loopbigcount)) * 255 / 100,0))  }\n")
        file.write(f"M104 S{round(Decimal(tsh+tih*loopbigcount),0)}\n")

        file.write(f";Layer {layer}\n")

        #Layer Marker Bottom Left
        file.write(f"G1 F{int(ps*60)} X-2 E{round(Decimal(corenermarker),5)}\n")
        file.write(f"G1 F{int(ps*60)} Y-2 E{round(Decimal(corenermarker),5)}\n")
        file.write(f"G1 F{int(ps*60)} X2 E{round(Decimal(corenermarker),5)}\n")
        file.write(f"G1 F{int(ps*60)} Y2 E{round(Decimal(corenermarker),5)}\n")


        #Begin 

        #Bottom
        file.write(f"G1 F{int(ps*60)} X10 E{round(Decimal(eValueresult),5)}\n")
        file.write(f"G1 E{round(Decimal(srd+ird*0),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G0 F{int(ts)*60} Y-10\n")
        file.write(f"G0 F{int(ts)*60} Y10\n")
        file.write(f"G1 E{round(Decimal(srd+ird*0),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G1 F{int(ps*60)} X10 E{round(Decimal(eValueresult),5)}\n")
        file.write(f"G1 E{round(Decimal(srd+ird*1),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G0 F{int(ts)*60} Y-10\n")
        file.write(f"G0 F{int(ts)*60} Y10\n")
        file.write(f"G1 E{round(Decimal(srd+ird*1),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G1 F{int(ps*60)} X10 E{round(Decimal(eValueresult),5)}\n")
        file.write(f"G1 E{round(Decimal(srd+ird*2),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G0 F{int(ts)*60} Y-10\n")
        file.write(f"G0 F{int(ts)*60} Y10\n")
        file.write(f"G1 E{round(Decimal(srd+ird*2),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G1 F{int(ps*60)} X10 E{round(Decimal(eValueresult),5)}\n")
        file.write(f"G1 E{round(Decimal(srd+ird*3),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G0 F{int(ts)*60} Y-10\n")
        file.write(f"G0 F{int(ts)*60} Y10\n")
        file.write(f"G1 E{round(Decimal(srd+ird*3),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G1 F{int(ps*60)} X10 E{round(Decimal(eValueresult),5)}\n")

        #Layer Marker Bottom Right
        file.write(f"G1 F{int(ps*60)} X1 E{round(Decimal(corenermarker),5)}\n")
        file.write(f"G1 F{int(ps*60)} Y-1 E{round(Decimal(corenermarker),5)}\n")
        file.write(f"G1 F{int(ps*60)} X-1 E{round(Decimal(corenermarker),5)}\n")
        file.write(f"G1 F{int(ps*60)} Y1 E{round(Decimal(corenermarker),5)}\n")

        #Right
        file.write(f"G1 F{int(ps*60)} Y10 E{round(Decimal(eValueresult),5)}\n")
        file.write(f"G1 E{round(Decimal(srd+ird*4),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G0 F{int(ts)*60} X10\n")
        file.write(f"G0 F{int(ts)*60} X-10\n")
        file.write(f"G1 E{round(Decimal(srd+ird*4),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G1 F{int(ps*60)} Y10 E{round(Decimal(eValueresult),5)}\n")
        file.write(f"G1 E{round(Decimal(srd+ird*5),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G0 F{int(ts)*60} X10\n")
        file.write(f"G0 F{int(ts)*60} X-10\n")
        file.write(f"G1 E{round(Decimal(srd+ird*5),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G1 F{int(ps*60)} Y10 E{round(Decimal(eValueresult),5)}\n")
        file.write(f"G1 E{round(Decimal(srd+ird*6),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G0 F{int(ts)*60} X10\n")
        file.write(f"G0 F{int(ts)*60} X-10\n")
        file.write(f"G1 E{round(Decimal(srd+ird*6),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G1 F{int(ps*60)} Y10 E{round(Decimal(eValueresult),5)}\n")
        file.write(f"G1 E{round(Decimal(srd+ird*7),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G0 F{int(ts)*60} X10\n")
        file.write(f"G0 F{int(ts)*60} X-10\n")
        file.write(f"G1 E{round(Decimal(srd+ird*7),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G1 F{int(ps*60)} Y10 E{round(Decimal(eValueresult),5)}\n")

        #Layer Marker Top Right
        file.write(f"G1 F{int(ps*60)} X1 E{round(Decimal(corenermarker),5)}\n")
        file.write(f"G1 F{int(ps*60)} Y1 E{round(Decimal(corenermarker),5)}\n")
        file.write(f"G1 F{int(ps*60)} X-1 E{round(Decimal(corenermarker),5)}\n")
        file.write(f"G1 F{int(ps*60)} Y-1 E{round(Decimal(corenermarker),5)}\n")

        #Top
        file.write(f"G1 F{int(ps*60)} X-10 E{round(Decimal(eValueresult),5)}\n")
        file.write(f"G1 E{round(Decimal(srd+ird*8),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G0 F{int(ts)*60} Y10\n")
        file.write(f"G0 F{int(ts)*60} Y-10\n")
        file.write(f"G1 E{round(Decimal(srd+ird*8),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G1 F{int(ps*60)} X-10 E{round(Decimal(eValueresult),5)}\n")
        file.write(f"G1 E{round(Decimal(srd+ird*9),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G0 F{int(ts)*60} Y10\n")
        file.write(f"G0 F{int(ts)*60} Y-10\n")
        file.write(f"G1 E{round(Decimal(srd+ird*9),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G1 F{int(ps*60)} X-10 E{round(Decimal(eValueresult),5)}\n")
        file.write(f"G1 E{round(Decimal(srd+ird*10),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G0 F{int(ts)*60} Y10\n")
        file.write(f"G0 F{int(ts)*60} Y-10\n")
        file.write(f"G1 E{round(Decimal(srd+ird*10),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G1 F{int(ps*60)} X-10 E{round(Decimal(eValueresult),5)}\n")
        file.write(f"G1 E{round(Decimal(srd+ird*11),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G0 F{int(ts)*60} Y10\n")
        file.write(f"G0 F{int(ts)*60} Y-10\n")
        file.write(f"G1 E{round(Decimal(srd+ird*11),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G1 F{int(ps*60)} X-10 E{round(Decimal(eValueresult),5)}\n")

        #Layer Marker Top Left
        file.write(f"G1 F{int(ps*60)} X-1 E{round(Decimal(corenermarker),5)}\n")
        file.write(f"G1 F{int(ps*60)} Y1 E{round(Decimal(corenermarker),5)}\n")
        file.write(f"G1 F{int(ps*60)} X1 E{round(Decimal(corenermarker),5)}\n")
        file.write(f"G1 F{int(ps*60)} Y-1 E{round(Decimal(corenermarker),5)}\n")

        #Left
        file.write(f"G1 F{int(ps*60)} Y-10 E{round(Decimal(eValueresult),5)}\n")
        file.write(f"G1 E{round(Decimal(srd+ird*12),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G0 F{int(ts)*60} X-10\n")
        file.write(f"G0 F{int(ts)*60} X10\n")
        file.write(f"G1 E{round(Decimal(srd+ird*12),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G1 F{int(ps*60)} Y-10 E{round(Decimal(eValueresult),5)}\n")
        file.write(f"G1 E{round(Decimal(srd+ird*13),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G0 F{int(ts)*60} X-10\n")
        file.write(f"G0 F{int(ts)*60} X10\n")
        file.write(f"G1 E{round(Decimal(srd+ird*13),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G1 F{int(ps*60)} Y-10 E{round(Decimal(eValueresult),5)}\n")
        file.write(f"G1 E{round(Decimal(srd+ird*14),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G0 F{int(ts)*60} X-10\n")
        file.write(f"G0 F{int(ts)*60} X10\n")
        file.write(f"G1 E{round(Decimal(srd+ird*14),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G1 F{int(ps*60)} Y-10 E{round(Decimal(eValueresult),5)}\n")
        file.write(f"G1 E{round(Decimal(srd+ird*15),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G0 F{int(ts)*60} X-10\n")
        file.write(f"G0 F{int(ts)*60} X10\n")
        file.write(f"G1 E{round(Decimal(srd+ird*15),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
        file.write(f"G1 F{int(ps*60)} Y-10 E{round(Decimal(eValueresult),5)}\n")

        #Zup layer height
        file.write(f"G1 Z{lh}\n")
             
#       loopbigcount = loopbigcount +1
        layer = layer + 1


        for loopsmall in range(int(lt)):

            file.write(f";Layer {layer}\n")
            #Bottom
            file.write(f"G1 F{int(ps*60)} X10 E{round(Decimal(eValueresult),5)}\n")
            file.write(f"G1 E{round(Decimal(srd+ird*0),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G0 F{int(ts)*60} Y-10\n")
            file.write(f"G0 F{int(ts)*60} Y10\n")
            file.write(f"G1 E{round(Decimal(srd+ird*0),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G1 F{int(ps*60)} X10 E{round(Decimal(eValueresult),5)}\n")
            file.write(f"G1 E{round(Decimal(srd+ird*1),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G0 F{int(ts)*60} Y-10\n")
            file.write(f"G0 F{int(ts)*60} Y10\n")
            file.write(f"G1 E{round(Decimal(srd+ird*1),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G1 F{int(ps*60)} X10 E{round(Decimal(eValueresult),5)}\n")
            file.write(f"G1 E{round(Decimal(srd+ird*2),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G0 F{int(ts)*60} Y-10\n")
            file.write(f"G0 F{int(ts)*60} Y10\n")
            file.write(f"G1 E{round(Decimal(srd+ird*2),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G1 F{int(ps*60)} X10 E{round(Decimal(eValueresult),5)}\n")
            file.write(f"G1 E{round(Decimal(srd+ird*3),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G0 F{int(ts)*60} Y-10\n")
            file.write(f"G0 F{int(ts)*60} Y10\n")
            file.write(f"G1 E{round(Decimal(srd+ird*3),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G1 F{int(ps*60)} X10 E{round(Decimal(eValueresult),5)}\n")

            #Right
            file.write(f"G1 F{int(ps*60)} Y10 E{round(Decimal(eValueresult),5)}\n")
            file.write(f"G1 E{round(Decimal(srd+ird*4),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G0 F{int(ts)*60} X10\n")
            file.write(f"G0 F{int(ts)*60} X-10\n")
            file.write(f"G1 E{round(Decimal(srd+ird*4),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G1 F{int(ps*60)} Y10 E{round(Decimal(eValueresult),5)}\n")
            file.write(f"G1 E{round(Decimal(srd+ird*5),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G0 F{int(ts)*60} X10\n")
            file.write(f"G0 F{int(ts)*60} X-10\n")
            file.write(f"G1 E{round(Decimal(srd+ird*5),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G1 F{int(ps*60)} Y10 E{round(Decimal(eValueresult),5)}\n")
            file.write(f"G1 E{round(Decimal(srd+ird*6),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G0 F{int(ts)*60} X10\n")
            file.write(f"G0 F{int(ts)*60} X-10\n")
            file.write(f"G1 E{round(Decimal(srd+ird*6),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G1 F{int(ps*60)} Y10 E{round(Decimal(eValueresult),5)}\n")
            file.write(f"G1 E{round(Decimal(srd+ird*7),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G0 F{int(ts)*60} X10\n")
            file.write(f"G0 F{int(ts)*60} X-10\n")
            file.write(f"G1 E{round(Decimal(srd+ird*7),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G1 F{int(ps*60)} Y10 E{round(Decimal(eValueresult),5)}\n")

            #Top
            file.write(f"G1 F{int(ps*60)} X-10 E{round(Decimal(eValueresult),5)}\n")
            file.write(f"G1 E{round(Decimal(srd+ird*8),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G0 F{int(ts)*60} Y10\n")
            file.write(f"G0 F{int(ts)*60} Y-10\n")
            file.write(f"G1 E{round(Decimal(srd+ird*8),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G1 F{int(ps*60)} X-10 E{round(Decimal(eValueresult),5)}\n")
            file.write(f"G1 E{round(Decimal(srd+ird*9),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G0 F{int(ts)*60} Y10\n")
            file.write(f"G0 F{int(ts)*60} Y-10\n")
            file.write(f"G1 E{round(Decimal(srd+ird*9),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G1 F{int(ps*60)} X-10 E{round(Decimal(eValueresult),5)}\n")
            file.write(f"G1 E{round(Decimal(srd+ird*10),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G0 F{int(ts)*60} Y10\n")
            file.write(f"G0 F{int(ts)*60} Y-10\n")
            file.write(f"G1 E{round(Decimal(srd+ird*10),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G1 F{int(ps*60)} X-10 E{round(Decimal(eValueresult),5)}\n")
            file.write(f"G1 E{round(Decimal(srd+ird*11),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G0 F{int(ts)*60} Y10\n")
            file.write(f"G0 F{int(ts)*60} Y-10\n")
            file.write(f"G1 E{round(Decimal(srd+ird*11),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G1 F{int(ps*60)} X-10 E{round(Decimal(eValueresult),5)}\n")

            #Left
            file.write(f"G1 F{int(ps*60)} Y-10 E{round(Decimal(eValueresult),5)}\n")
            file.write(f"G1 E{round(Decimal(srd+ird*12),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G0 F{int(ts)*60} X-10\n")
            file.write(f"G0 F{int(ts)*60} X10\n")
            file.write(f"G1 E{round(Decimal(srd+ird*12),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G1 F{int(ps*60)} Y-10 E{round(Decimal(eValueresult),5)}\n")
            file.write(f"G1 E{round(Decimal(srd+ird*13),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G0 F{int(ts)*60} X-10\n")
            file.write(f"G0 F{int(ts)*60} X10\n")
            file.write(f"G1 E{round(Decimal(srd+ird*13),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G1 F{int(ps*60)} Y-10 E{round(Decimal(eValueresult),5)}\n")
            file.write(f"G1 E{round(Decimal(srd+ird*14),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G0 F{int(ts)*60} X-10\n")
            file.write(f"G0 F{int(ts)*60} X10\n")
            file.write(f"G1 E{round(Decimal(srd+ird*14),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G1 F{int(ps*60)} Y-10 E{round(Decimal(eValueresult),5)}\n")
            file.write(f"G1 E{round(Decimal(srd+ird*15),2) * -1} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G0 F{int(ts)*60} X-10\n")
            file.write(f"G0 F{int(ts)*60} X10\n")
            file.write(f"G1 E{round(Decimal(srd+ird*15),2)} F{round(Decimal((srs+irs*loopbigcount) * 60),2)}\n")
            file.write(f"G1 F{int(ps*60)} Y-10 E{round(Decimal(eValueresult),5)}\n")

            file.write(f"G1 Z{lh}\n")
            layer = layer + 1

        loopbigcount = loopbigcount +1


    #End Game

    #Raise 5mm
    file.write(f"G1 Z5\n")    
    #Absolute Position
    file.write(f"G90\n")
    #Home X Y
    file.write(f"G28 X0 Y0\n")
    #Turn off Steppers
    file.write(f"M84\n")
    #Turn off Fan
    file.write(f"M107\n")
    #Turn off Hotend
    file.write(f"M104 S0\n")
    #Turn off Bed
    file.write(f"M140 S0\n")

    file.seek(0)
    return Response( file, mimetype="text/plain", headers={"Content-disposition": "attachment; filename=calibration.gcode"})



