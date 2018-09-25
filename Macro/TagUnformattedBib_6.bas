' Declaration of Types
Type ReferenceType
    Tag As String
    Patterns As Collection
End Type

' This subroutine tags each record in an unformatted bibliography
' in order to allow the record to be recognized by our EndNote filter
Sub TagUnformattedBib()
    'TagItalic
    TagRecordBegin
    TagRecordRefType
End Sub

' This macro selects each newline and if that newline is a record (i.e. lenght > 1 char),
' it tags the line with a "x--" at the start of the line
Sub TagRecordBegin()
    ' Move cursor to top of the page
    Selection.GoTo What:=wdGoToPage, Which:=wdGoToFirst

    For i = 1 To ActiveDocument.Paragraphs.Count
        Dim currentPara As Object
        Set currentPara = ActiveDocument.Paragraphs(i)
        currentPara.Range.Select
        If Len(Selection.Text) > 1 Then
            Selection.InsertBefore ("x--")
        End If
    Next i

    ' Move cursor to top of the page
    Selection.GoTo What:=wdGoToPage, Which:=wdGoToFirst
End Sub

' This subroutine takes each record and tries to tag it with the ReferenceType it matches based
' on the patterns defined for each ReferenceType above. If a record matches more than one
' refType, it signals a conflict by highlighting the line in yellow. If it matches no patterns
' at all, it highlights is red, signalling failure.
Sub TagRecordRefType()
    ' Move cursor to top of the page
    Selection.GoTo What:=wdGoToPage, Which:=wdGoToFirst
    'To keep count of how many records failed
    Dim failCount As Integer
    failCount = 0

    ' Define book ref type
    Dim refTypeBook As ReferenceType
    refTypeBook.Tag = "DT:BK."
    Set refTypeBook.Patterns = New Collection

    ' Define bookSec ref type
    Dim refTypeBookSec As ReferenceType
    refTypeBookSec.Tag = "DT:BS."
    Set refTypeBookSec.Patterns = New Collection

    ' Define JA ref type
    Dim refTypeJournal As ReferenceType
    refTypeJournal.Tag = "DT:JA."
    Set refTypeJournal.Patterns = New Collection

    ' Define MS ref type
    Dim refTypeMS As ReferenceType
    refTypeMS.Tag = "DT:MS."
    Set refTypeMS.Patterns = New Collection

    ' Regex patterns for Books:
    ' -------------------------
    ' Basic Book
    refTypeBook.Patterns.Add "x--*[.,] <i>*</i>. *, [0-9n][0-9.][0-9d]*."
    refTypeBook.Patterns.Add "x--*[.,] ([et][dr].*) <i>*</i>. *, [0-9n][0-9.][0-9d]*."
    refTypeBook.Patterns.Add "x--*[.,] ([et][dr]s.*) <i>*</i>. *, [0-9n][0-9.][0-9d]*."
    ' Book with other info like subtitle, ed., trans., etc...
    refTypeBook.Patterns.Add "x--*[.,] <i>*</i>, *. *, [0-9n][0-9.][0-9d]*.*"
    refTypeBook.Patterns.Add "x--*[.,] <i>*</i>, *, *ed*. [0-9n][0-9.][0-9d]*.*"

    ' Regex patterns for Book Section:
    ' --------------------------------
    ' Basic Book Section
    refTypeBookSec.Patterns.Add "x--*. " & "[" & ChrW(8216) & ChrW(34) & ChrW(8220) & "]" & "*" & "[" & ChrW(8217) & ChrW(34) & ChrW(8221) & "]" & "* [iI]n <i>*</i>[.,] *. *####*.*"
    ' Chapter in a book
    refTypeBookSec.Patterns.Add "x--*. " & "[" & ChrW(8216) & ChrW(34) & ChrW(8220) & "]" & "*" & "[" & ChrW(8217) & ChrW(34) & ChrW(8221) & "]" & "* [iI]n *<i>*</i>[.,] [eE][Dd]. *. *, [0-9n][0-9.][0-9d]*."
    refTypeBookSec.Patterns.Add "x--*. " & "[" & ChrW(8216) & ChrW(34) & ChrW(8220) & "]" & "*" & "[" & ChrW(8217) & ChrW(34) & ChrW(8221) & "]" & "* [iI]n *<i>*</i>[.,] *, [0-9n][0-9.][0-9d]*."
    ' Book Section Variation
    refTypeBookSec.Patterns.Add "x--*. " & "[" & ChrW(8216) & ChrW(34) & ChrW(8220) & "]" & "*" & "[" & ChrW(8217) & ChrW(34) & ChrW(8221) & "]" & "* [iI]n *ed.* <i>*</i>. *, [0-9n][0-9.][0-9d]*."

    ' Regex patterns for Journal Articles:
    ' ------------------------------------
    ' Basic Journal Article with issue no. and volume'
    refTypeJournal.Patterns.Add "x--*. ""*."" <i>*</i> #*, no. #* (#*): #*."
    ' Journal Article with volume as vol. and without issue no.
    refTypeJournal.Patterns.Add "x--*. " & "[" & ChrW(8216) & ChrW(34) & ChrW(8220) & "]" & "*" & "[" & ChrW(8217) & ChrW(34) & ChrW(8221) & "]" & ", <i>*</i>, vol. *, *[Pp]. #*."
    ' Journal Article with "issueNo (date): pages"
    refTypeJournal.Patterns.Add "x--*. " & "[" & ChrW(8216) & ChrW(34) & ChrW(8220) & "]" & "*" & "[" & ChrW(8217) & ChrW(34) & ChrW(8221) & "]" & "* <i>*</i> *#* (#*#): #*#."
    refTypeJournal.Patterns.Add "x--*. " & "[" & ChrW(8216) & ChrW(34) & ChrW(8220) & "]" & "*" & "[" & ChrW(8217) & ChrW(34) & ChrW(8221) & "]" & "* <i>*</i>, *, no. #* (#*), *[pP]. #*."
    refTypeJournal.Patterns.Add "x--*. " & "[" & ChrW(8216) & ChrW(34) & ChrW(8220) & "]" & "*" & "[" & ChrW(8217) & ChrW(34) & ChrW(8221) & "]" & "* <i>*</i>, *# (#*), *[pP]. #*."
    refTypeJournal.Patterns.Add "x--*. " & "[" & ChrW(8216) & ChrW(34) & ChrW(8220) & "]" & "*" & "[" & ChrW(8217) & ChrW(34) & ChrW(8221) & "]" & "* <i>*</i> (*), *# (#*), *[pP]. #*."
    refTypeJournal.Patterns.Add "x--*. " & "[" & ChrW(8216) & ChrW(34) & ChrW(8220) & "]" & "*" & "[" & ChrW(8217) & ChrW(34) & ChrW(8221) & "]" & "* <i>*, #</i> (#*), *[pP]. #*."
    refTypeJournal.Patterns.Add "x--*. " & "[" & ChrW(8216) & ChrW(34) & ChrW(8220) & "]" & "*" & "[" & ChrW(8217) & ChrW(34) & ChrW(8221) & "]" & "* <i>*Journal*</i> (#*), *[Pp]. #*."
    

    ' Regex patterns for Manuscripts:
    ' -------------------------------
    refTypeMS.Patterns.Add "x--*. <i>*</i>. [A-Z]*, [A-Z]*."
    refTypeMS.Patterns.Add "x--*. <i>*</i>[.,]* MS *."
    refTypeMS.Patterns.Add "x--*. <i>*</i>[.,]* [mM]anuscript*."
    
    ' Define reference type collection
    Dim refTypes(1 To 4) As ReferenceType
    refTypes(1) = refTypeBook
    refTypes(2) = refTypeJournal
    refTypes(3) = refTypeMS
    refTypes(4) = refTypeBookSec

    ' Loop through each newline (which should ideally correspond to each record)
    For i = 1 To ActiveDocument.Paragraphs.Count

        ' Select current record and prepare it for parsing
        Dim currentPara As Object
        Set currentPara = ActiveDocument.Paragraphs(i)
        currentPara.Range.Select
        ' Only parse if it is an actual record i.e. no empty newlines
        If Len(Selection.Text) > 1 Then

            ' Variables to store whether a match and/or a conflict has taken place
            Dim refMatch As Boolean
            refMatch = False
            Dim conflict As Boolean
            conflict = False
            ' Trim off whitespace and empty newlines from the record
            Dim record As String
            record = Trim(Replace(Selection.Text, Chr(13), ""))

            ' RECORD MATCHING BEGINS IN THIS NESTED LOOP:
            ' -------------------------------------------
            ' Loop through each reference type (refType) that has been defined
            For j = LBound(refTypes) To UBound(refTypes)
                Dim refType As ReferenceType
                refType = refTypes(j)

                ' Loop through each pattern that has been registered for that refType
                For Each Pattern In refType.Patterns
                    If record Like Pattern Then

                        ' If this record had already matched a DIFFERENT refType in the past, signal a conflict
                        If refMatch Then
                            conflict = True
                            Selection.Range.HighlightColorIndex = wdYellow
                        ' If no match yet, then just register the match
                        Else
                            refMatch = True
                        End If

                        ' Tag the record with using the tag of the refType it was matched to
                        Selection.InsertBefore (refType.Tag & Chr(11))
                        ' Selection.Collapse Direction:=wdCollapseStart

                        ' Selection.InsertBreak Type:=wdLineBreak
                        

                        ' No need to try out other patterns for that same refType if a match is found
                        Exit For
                    End If
                Next Pattern
            Next j

            ' If this record didn't match any refType's patterns, highlight it red and increase count
            If Not refMatch Then
                Selection.Range.HighlightColorIndex = wdRed
                failCount = failCount + 1
            End If
        End If
    Next i

    ' Move cursor to top again and print count of failed records, then exit
    Selection.GoTo What:=wdGoToPage, Which:=wdGoToFirst
    Debug.Print failCount
End Sub

' This subroutine finds tags italic text between <i> and </i> characters
' It excludes spaces and punctuation marks, but includes paranthesis
' TODO: Don't tag if empty i.e. no instance of "<i></i>"
Sub TagItalic()
    ' Move cursor to top of the page
    Selection.GoTo What:=wdGoToPage, Which:=wdGoToFirst

    ' Find text with Italic formatting and replace with non-Italic formatting
    With Selection.Find
        .ClearFormatting
        .Text = ""
        .Font.Italic = True
        With .Replacement
            .Text = ""
            .ClearFormatting
            .Font.Italic = False
        End With
    End With

    ' Run this loop until all instances of italic text haven't been tagged
    Do While Selection.Find.Execute(Replace:=wdReplaceOne) = True

        ' Starting tag: <i>
        ' --------------------------------------
        ' Include paranthesis in the italic tag
        Do While (Selection.Previous = "(")
            Selection.MoveStart Count:=-1
        Loop
        ' Avoid tagging punctuation marks and spaces as italic
        Do While (Selection.Previous.Next = ".") Or (Selection.Previous.Next = ",") Or (Selection.Previous.Next = " ")
            Selection.MoveStart
        Loop
        ' Insert the <i> tag and unselect the italic text
        Selection.InsertBefore ("<i>")
        Selection.Move
    
        ' Ending tag: </i>
        ' --------------------------------------
        ' Avoid tagging punctuation marks and spaces as italic
        Do While (Selection.Previous = ".") Or (Selection.Previous = ",") Or (Selection.Previous = " ")
            Selection.MoveLeft
        Loop
        ' Include paranthesis in the italic tag
        Do While (Selection.Next.Previous = ")")
            Selection.MoveRight
        Loop

        ' If tag is not empty, add ending tag
        ' If the tag is empty, discard the entire tag,
        If (Selection.Previous(Count:=3) = "<") And (Selection.Previous(Count:=2) = "i") And (Selection.Previous(Count:=1) = ">") Then
            Selection.MoveStart Count:=-3
            Selection.Delete
        Else
            ' Insert the </i> tag and unselect
            Selection.InsertBefore ("</i>")
            Selection.Move
        End If
    Loop

    ' Move cursor to top of the page
    Selection.GoTo What:=wdGoToPage, Which:=wdGoToFirst
End Sub
