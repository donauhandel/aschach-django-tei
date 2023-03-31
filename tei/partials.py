from xml.sax.saxutils import escape, unescape


TEI_NSMAP = {
    'tei': "http://www.tei-c.org/ns/1.0",
    'xml': "http://www.w3.org/XML/1998/namespace",
}

TEI_STUMP = """
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
      <fileDesc>
         <titleStmt>
            <title type="main"></title>
            <title type="sub">Donauhandel</title>
            <respStmt>
               <resp>Projektleitung, Datenerhebung</resp>
               <persName key="https://d-nb.info/gnd/13140007X">
                  <forename>Peter</forename>
                  <surname>Rauscher</surname>
               </persName>
            </respStmt>
            <respStmt>
               <resp>Datenerhebung</resp>
               <persName key="https://d-nb.info/gnd/1031446176">
                  <forename>Andrea</forename>
                  <surname>Serles</surname>
               </persName>
            </respStmt>
            <respStmt>
               <resp>Datenmodellierung und Aufsetzen einer Datenbankapplikation zur Datenerhebung</resp>
               <persName key="https://d-nb.info/gnd/103048337X">
                  <forename>Beate</forename>
                  <surname>Pamperl</surname>
               </persName>
            </respStmt>
            <respStmt>
               <resp>Datenmodellierung und Datenkonvertierung nach TEI</resp>
               <persName key="https://d-nb.info/gnd/1043833846">
                  <forename>Peter</forename>
                  <surname>Andorfer</surname>
               </persName>
            </respStmt>
         </titleStmt>
         <publicationStmt>
            <authority>
               <persName key="https://d-nb.info/gnd/13140007X">
                  <forename>Peter</forename>
                  <surname>Rauscher</surname>
               </persName>
            </authority>
            <availability>
               <licence target="https://creativecommons.org/licenses/by/4.0/">CC-BY</licence>
            </availability>
         </publicationStmt>
         <sourceDesc>
            <msDesc>
               <msIdentifier>
                  <institution key="https://d-nb.info/gnd/2020619-7">Oberösterreichisches Landesarchiv (OÖLA)</institution>
                  <repository>Depot Harrach</repository>
                  <idno/>
               </msIdentifier>
               <msContents>
                  <msItem/>
               </msContents>
               <history>
                  <origin/>
               </history>
            </msDesc>
         </sourceDesc>
      </fileDesc>
     <encodingDesc>
        <ab>Der vorliegende Datensatz wurde von Peter Rauscher und seinen Projektmitarbeiter*Innen anhand der im tei:msDesc Element beschriebener Quelle mit Hilfe einer von Beate Pamperl erstellten Datenbankapplikation erhoben und als Datensatz in eine MySQL-Datenbank gespeichert. Dieser Datensatz wurde mittels einer von Peter Andorfer entwickelten Python/Django Web-Applikation in das vorliegende TEI Dokument transformiert</ab>
     </encodingDesc>
  </teiHeader>
   <facsimile/>
  <text>
      <body/>
      <back/>
  </text>
</TEI>
"""


def custom_escape(somestring):
    un_escaped = unescape(somestring)
    return escape(un_escaped)
