<?xml version="1.0" encoding="iso-8859-1"?>
<xsl:stylesheet version="1.0" 
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:xlink="http://www.w3.org/1999/xlink"
		xmlns="http://www.w3.org/2000/svg"
		>
<!-- Paramètres changable -->
  <xsl:variable name="ligne_select" >L1544644</xsl:variable>
  <xsl:variable name="svg_width" select="5000"/>
  <xsl:variable name="svg_height" select="800"/>
<!-- Fin -->
	
  <xsl:output
      method="xml"
      indent="yes"
      standalone="no"
      doctype-public="-//W3C//DTD SVG 1.1//EN"
      doctype-system="http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"
      media-type="image/svg" />		


  <xsl:template match="/">
    <svg xmlns="http://www.w3.org/2000/svg" width="{$svg_width}" height="{$svg_height}" >
      <rect x="0" y="0" width="{$svg_width}" height="{$svg_height}" fill="white"/>  
      <xsl:apply-templates/>
    </svg>
  </xsl:template>
  
 
  <xsl:template match="metro"> 
     <xsl:apply-templates select="ligne[@id = $ligne_select]"/>
  </xsl:template>

  
  <xsl:template match="ligne"> 
    <text transform="translate (10, 40) "
	font-family="Verdana" font-size="35" fill="black">
	Ligne : <xsl:value-of select="@short_name"/>
    </text> 
  <xsl:apply-templates select="nom_complet"/> 
  <xsl:apply-templates select="route"/> 
  </xsl:template>
  
  <xsl:template match="nom_complet"> 
    <text transform="translate (10, 100) "
	font-family="Verdana" font-size="35" fill="black">
	Nom Complet : <xsl:value-of select="first"/> - <xsl:value-of select="last"/>
    </text> 
  </xsl:template>
  <xsl:template match="route"> 
    <xsl:choose>
	<xsl:when test="position()=1">
		<xsl:apply-templates select="arret"/> 
	</xsl:when>
    </xsl:choose>
    
  </xsl:template>
  <xsl:template match="arret"> 
  	<xsl:variable name="idref" select="@idref"/>
  	<!-- Verifie si derniere station -->
          <xsl:choose>
		  <xsl:when test="position()!=last()">
		  <line x1="{150*position()}" y1="500" x2="{150*(position()+1)}" y2="500"
		  stroke="black" stroke-width="25" stroke-linecap="round"/>
		  <line x1="{150*position()}" y1="500" x2="{150*(position()+1)}" y2="500"
		  stroke="green" stroke-width="18" stroke-linecap="round"/>
		  </xsl:when>
          </xsl:choose>
       <!-- Nom de la station -->
        <text transform="translate ({150*position()}, 450) rotate(-45)"
	font-family="Verdana" font-size="35" fill="black">
	<xsl:value-of select="ancestor::*/station[@id = $idref]/station_name"/>
    	</text> 
    	<!-- Apparence d'une station -->
          <xsl:call-template name="correspondance">
             <xsl:with-param name="x" select="150*position()"/>
             <xsl:with-param name="y" select="500"/>
             <xsl:with-param name="id" select="@idref"/>
          </xsl:call-template>  
  </xsl:template>
  <xsl:template name="correspondance"> 
  	<xsl:param name="x"/>
  	<xsl:param name="y"/>
  	<xsl:param name="id"/>
    	<xsl:choose>
	      <xsl:when test="count(ancestor::*/station[@id = $id]/lignes/lig)>1">
	           <line x1="{$x}" y1="{$y}" x2="{$x}" y2="{$y+100}"
		   stroke="black" stroke-width="2"/>
		   <circle cx="{$x}" cy="{$y}" r="30"
          	   fill="white" stroke="black" stroke-width="5"/>
          	   <xsl:for-each select="ancestor::*/station[@id = $id]/lignes/lig[not(@idref=$ligne_select)]">	   	
          	   	<circle cx="{$x}" cy="{$y+position()*60 + 50}" r="30"
          	   	fill="blue"/>
          	   	<text x="{$x}" y="{$y+position()*60 + 60}" text-anchor="middle" font-family="Verdana" font-size="30" font-weight="bold" fill="white">
		    	<xsl:variable name="idref" select="@idref"/>
			<xsl:value-of select="ancestor::*/ligne[@id = $idref]/@short_name"/>
		    	</text> 
          	   </xsl:for-each>
	      </xsl:when>
	      <xsl:when test="count(ancestor::*/station[@id = $id]/lignes/lig)=1">
		   <circle cx="{150*position()}" cy="500" r="30"
          	   fill="green" stroke="black" stroke-width="5"/>
	      </xsl:when>
        </xsl:choose>
  </xsl:template>
  
</xsl:stylesheet>
