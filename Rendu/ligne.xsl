<?xml version="1.0" encoding="iso-8859-1"?>
<xsl:stylesheet version="1.0" 
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:xlink="http://www.w3.org/1999/xlink"
		xmlns="http://www.w3.org/2000/svg"
		>
<!-- Paramètres changable -->
  <xsl:variable name="ligne_select" >L2280400</xsl:variable>
  <xsl:variable name="svg_width" select="5000"/>
  <xsl:variable name="svg_height" select="1000"/>
<!-- Fin -->
	
	
	
	
		
  <xsl:output
      method="xml"
      indent="yes"
      standalone="no"
      doctype-public="-//W3C//DTD SVG 1.1//EN"
      doctype-system="http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd"
      media-type="image/svg" />		


<xsl:key name="idstation" match="station" use="@id"/>
<xsl:key name="idligne" match="ligne" use="@id"/>

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
  <xsl:apply-templates select="trajet">
     <xsl:with-param name="routes" select="count(route)"/>
  </xsl:apply-templates>
  </xsl:template>
  
  <xsl:template match="nom_complet"> 
    <text transform="translate (10, 100) "
	font-family="Verdana" font-size="35" fill="black">
	Nom Complet : <xsl:value-of select="first"/> - <xsl:value-of select="last"/>
    </text> 
  </xsl:template>
  <xsl:template match="trajet"> 
  	<xsl:param name="routes"/>
  	
	<xsl:apply-templates select="arret">
     	    <xsl:with-param name="routes" select="$routes"/>
  	</xsl:apply-templates>
  </xsl:template>
  <xsl:template match="arret"> 
  	<xsl:param name="routes"/>
  	<!-- Verifie si derniere station -->
          <xsl:choose>
		  <xsl:when test="position()!=last()">
		  <line x1="{150*position()}" y1="600" x2="{150*(position()+1)}" y2="600"
		  stroke="black" stroke-width="25" stroke-linecap="round"/>
		  <line x1="{150*position()}" y1="600" x2="{150*(position()+1)}" y2="600"
		  stroke="green" stroke-width="18" stroke-linecap="round"/>
		  </xsl:when>
          </xsl:choose>
    	<!-- Apparence d'une station -->
    	
	<xsl:apply-templates select="station"> 
	     <xsl:with-param name="x" select="150*position()"/>
             <xsl:with-param name="routes" select="$routes"/>
        </xsl:apply-templates>
  </xsl:template>
  <xsl:template match="station"> 
  	<xsl:param name="x"/>
  	<xsl:param name="routes"/>
  	<xsl:variable name="y"> 
  	    <xsl:choose>
  	    	<xsl:when test="$routes != count(route)">
  		    <xsl:value-of select="300 * position()"/>
  		</xsl:when>
     		<xsl:otherwise>
       	    <xsl:value-of select="450"/>
     		</xsl:otherwise>
  	    </xsl:choose>
  	</xsl:variable>
    	<!-- Nom de la station -->
        <text transform="translate ({$x}, {$y - 50}) rotate(-45)"
	font-family="Verdana" font-size="35" fill="black">
	<xsl:value-of select="key('idstation',@idref)/station_name"/>
	<xsl:value-of select="count(route)"/>
	<xsl:value-of select="$x"/>
    	</text> 
    	<!-- Cercle d'un arret -->
    	<xsl:choose>
    		<!-- Quand il y a une correspondance -->
	      <xsl:when test="count(key('idstation',@idref)/lignes/lig)>1">
	           <line x1="{$x}" y1="{$y}" x2="{$x}" y2="{$y+100}"
		   stroke="black" stroke-width="2"/>
		   <circle cx="{$x}" cy="{$y}" r="30"
          	   fill="white" stroke="black" stroke-width="5"/>
          	   <xsl:for-each select="key('idstation',@idref)/lignes/lig[not(@idref=$ligne_select)]">	   	
          	   	<circle cx="{$x}" cy="{$y+position()*60 + 50}" r="30"
          	   	fill="blue"/>
          	   	<text x="{$x}" y="{$y+position()*60 + 60}" text-anchor="middle" font-family="Verdana" font-size="30" font-weight="bold" fill="white">
		    	<xsl:variable name="idref" select="@idref"/>
			<xsl:value-of select="key('idligne',$idref)/@short_name"/>
		    	</text> 
          	   </xsl:for-each>
	      </xsl:when>
	      <!-- Quand il n'y a pas une correspondance -->
	      <xsl:when test="count(key('idstation',@idref)/lignes/lig)=1">
		   <circle cx="{$x}" cy="{$y}" r="30"
          	   fill="green" stroke="black" stroke-width="5"/>
	      </xsl:when>
        </xsl:choose>
  </xsl:template>
</xsl:stylesheet>
