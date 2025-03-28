<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="xml" indent="yes" omit-xml-declaration="yes" />
<xsl:template match="/ | node()">
      <DenmEtsi>
		  <gbcGacHeader>
			<basicHeader>
			  <version>1</version>
			  <nextHeader>1</nextHeader>
			  <reserved>0</reserved>
			  <lifeTime>
				<multiplier>19</multiplier>
				<base>0</base>
			  </lifeTime>
			  <remaingHop>1</remaingHop>
			</basicHeader>
			<commonHeader>
			  <nextHeader>2</nextHeader>
			  <reserved1>0</reserved1>
			  <headerType>4</headerType>
			  <headerSubType>0</headerSubType>
			  <traficClass>
				<scf>
				  <false/>
				</scf>
				<channelOffload>
				  <false/>
				</channelOffload>
				<tcID>0</tcID>
			  </traficClass>
			  <flags>
				<mobile>
				  <true/>
				</mobile>
				<reserved>0</reserved>
			  </flags>
			  <payloadLength>0</payloadLength>
			  <maxHopLimit>1</maxHopLimit>
			  <reserved2>0</reserved2>
			</commonHeader>
			<sequenceNumber>1</sequenceNumber>
			<reserved1>0</reserved1>
			<sopv>
			  <address>
				<configuration>
				  <manual/>
				</configuration>
				<stationType>0</stationType>
				<reserved>0</reserved>
				<mid>
				  <lsb>0</lsb>
				  <msb>0</msb>
				</mid>
			  </address>
			  <tst>##Timestamp##</tst>
			  <latitude>##Latitude##</latitude>
			  <longitude>##Longitude##</longitude>
			  <pai>
				<false/>
			  </pai>
			  <speed>-16383</speed>
			  <heading>0</heading>
			</sopv>
			<geoArea>
			  <lat>##Latitude##</lat>
			  <long>##Longitude##</long>
			  <distanceA>0</distanceA>
			  <distanceB>0</distanceB>
			  <angle>0</angle>
			</geoArea>
			<reserved2>0</reserved2>
		  </gbcGacHeader>
		  <btpb>
			<destinationPort>2002</destinationPort>
			<destinationPortInfo>0</destinationPortInfo>
		  </btpb>
		<xsl:apply-templates/>
	</DenmEtsi>
</xsl:template>

<xsl:template match="DENM">
    <denm>
        <xsl:apply-templates/>
    </denm>
</xsl:template>

<xsl:template match="DENM/header">
    <xsl:copy-of select="." />
</xsl:template>

<xsl:template match="DENM/denm/*|node()">
    <xsl:copy>
        <xsl:apply-templates/>
    </xsl:copy>
</xsl:template>

<xsl:template match="altitudeConfidence">
<xsl:copy>
<xsl:choose>
  <xsl:when test="text() = 0"><alt-000-01/></xsl:when>
  <xsl:when test="text() = 1"><alt-000-02/></xsl:when>
  <xsl:when test="text() = 2"><alt-000-05/></xsl:when>
  <xsl:when test="text() = 3"><alt-000-10/></xsl:when>
  <xsl:when test="text() = 4"><alt-000-20/></xsl:when>
  <xsl:when test="text() = 5"><alt-000-50/></xsl:when>
  <xsl:when test="text() = 6"><alt-001-00/></xsl:when>
  <xsl:when test="text() = 7"><alt-002-00/></xsl:when>
  <xsl:when test="text() = 8"><alt-005-00/></xsl:when>
  <xsl:when test="text() = 9"><alt-010-00/></xsl:when>
  <xsl:when test="text() = 10"><alt-020-00/></xsl:when>
  <xsl:when test="text() = 11"><alt-050-00/></xsl:when>
  <xsl:when test="text() = 12"><alt-100-00/></xsl:when>
  <xsl:when test="text() = 13"><alt-200-00/></xsl:when>
  <xsl:when test="text() = 14"><outOfRange/></xsl:when>
  <xsl:when test="text() = 15"><unavailable/></xsl:when>
  <xsl:otherwise><unavailable/></xsl:otherwise>
</xsl:choose>
</xsl:copy>
</xsl:template>
   
<xsl:template match="relevanceTrafficDirection ">
<xsl:copy>
<xsl:choose>
  <xsl:when test="text() = 0"><allTrafficDirections/></xsl:when>
  <xsl:when test="text() = 1"><upstreamTraffic/></xsl:when>
  <xsl:when test="text() = 2"><downstreamTraffic/></xsl:when>
  <xsl:when test="text() = 3"><oppositeTraffic/></xsl:when>
  <xsl:otherwise><allTrafficDirections/></xsl:otherwise>
</xsl:choose>
</xsl:copy>
</xsl:template>

<xsl:template match="relevanceDistance">
<xsl:copy>
<xsl:choose>
  <xsl:when test="text() = 0"><lessThan50m/></xsl:when>
  <xsl:when test="text() = 1"><lessThan100m/></xsl:when>
  <xsl:when test="text() = 2"><lessThan200m/></xsl:when>
  <xsl:when test="text() = 3"><lessThan500m/></xsl:when>
  <xsl:when test="text() = 4"><lessThan1000m/></xsl:when>
  <xsl:when test="text() = 5"><lessThan5km/></xsl:when>
  <xsl:when test="text() = 6"><lessThan10km/></xsl:when>
  <xsl:when test="text() = 7"><over10km/></xsl:when>
  <xsl:otherwise><over10km/></xsl:otherwise>
</xsl:choose>
</xsl:copy>
</xsl:template>

<xsl:template match="termination">
<xsl:copy>
<xsl:choose>
  <xsl:when test="text() = 0"><isCancellation/></xsl:when>
  <xsl:when test="text() = 1"><isNegation/></xsl:when>
  <xsl:when test="self::termination[isNegation]"><isNegation/></xsl:when>
</xsl:choose>
</xsl:copy>
</xsl:template>

 
</xsl:stylesheet>