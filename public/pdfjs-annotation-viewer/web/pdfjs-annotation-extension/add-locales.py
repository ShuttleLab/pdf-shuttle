#!/usr/bin/env python3
# Adds the site's UI languages to the third-party pdfjs-annotation-extension i18next
# resources, which ship only en/de/zh upstream. Run after re-vendoring the extension.
#
#   python3 add-locales.py
#
# Strategy (self-contained + idempotent):
#   1. Extract the upstream `en` translation (96 keys) straight from the bundle as the
#      authoritative key structure.
#   2. Prepend `lang:{translation:JSON.parse('<escaped>')}` for each language right after
#      `Oe={` (the i18next resources object).
#   3. Extend the `Ae` region->base map so region codes resolve (the extension routes any
#      lng longer than 2 chars through Ae, NOT i18next's own fallback): es-ES->es,
#      pt-BR->pt, zh-TW->zh-TW. Bare codes (ar/ja/ko/...) skip Ae and match Oe directly.
# Re-running is a no-op once patched.
import json, sys, re, os

BUNDLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdfjs-annotation-extension.js")
_src0 = open(BUNDLE, encoding="utf-8").read()
if re.search(r"\bar:\{translation:JSON\.parse", _src0):
    print("Already patched (ar resource present) — nothing to do.")
    sys.exit(0)
_m = re.search(r"en:\{translation:JSON\.parse\('(.+?)'\)\}", _src0, re.S)
assert _m, "could not locate upstream en translation in bundle"
EN = json.loads(_m.group(1).replace("\\'", "'").replace("\\\\", "\\"))

# Flat dotted-key translations. Keys must exactly mirror EN's 96 leaves.
# Date-format layout strings (dateFormat.*) are intentionally identical to EN — they are
# placeholder layouts, not prose. Placeholders {{...}} are preserved verbatim.
T = {}

T["es"] = {
"anno":"Comentario",
"annotations.select":"Seleccionar","annotations.highlight":"Resaltar","annotations.strikeout":"Tachar","annotations.underline":"Subrayar","annotations.rectangle":"Rectángulo","annotations.circle":"Círculo","annotations.freehand":"Mano alzada","annotations.freeHighlight":"Resaltado libre","annotations.freeText":"Texto","annotations.signature":"Firma","annotations.stamp":"Sello","annotations.note":"Nota","annotations.arrow":"Flecha","annotations.cloud":"Nube",
"toolbar.buttons.createSignature":"Crear firma","toolbar.buttons.uploadImage":"Subir imagen","toolbar.buttons.createStamp":"Crear sello",
"toolbar.message.selectPosition":"Seleccione una posición","toolbar.message.signatureArea":"Firma","toolbar.message.uploadArea":"Área de carga","toolbar.message.uploadHint":"Haga clic para subir o arrastre y suelte aquí {{format}}, tamaño máx. {{maxSize}}",
"editor.text.startTyping":"Empiece a escribir…",
"editor.stamp.stampText":"Texto del sello","editor.stamp.fontStyle":"Estilo de fuente","editor.stamp.fontFamily":"Tipo de fuente","editor.stamp.textColor":"Color del texto","editor.stamp.backgroundColor":"Color de fondo","editor.stamp.borderColor":"Color del borde","editor.stamp.borderStyle":"Estilo del borde","editor.stamp.timestampText":"Texto de marca de tiempo","editor.stamp.customTimestamp":"Texto personalizado","editor.stamp.username":"Nombre de usuario","editor.stamp.date":"Fecha","editor.stamp.time":"Hora","editor.stamp.dateFormat":"Formato de fecha","editor.stamp.solid":"Sólido","editor.stamp.dashed":"Discontinuo","editor.stamp.defaultText":"Borrador",
"normal.ok":"Aceptar","normal.cancel":"Cancelar","normal.clear":"Borrar","normal.fileSizeLimit":"El tamaño del archivo supera el límite de {{value}}","normal.deleteConfirm":"¿Seguro que desea eliminar?","normal.yes":"Sí","normal.no":"No","normal.example":"p. ej. ","normal.color":"Color","normal.export":"Exportar","normal.save":"Guardar","normal.reply":"Responder","normal.edit":"Editar","normal.delete":"Eliminar","normal.confirm":"Confirmar","normal.unknownUser":"Usuario desconocido","normal.processing":"Procesando, espere...","normal.filter":"Filtrar","normal.author":"Autor","normal.type":"Tipo","normal.selectAll":"Seleccionar todo","normal.more":"Más","normal.draw":"Dibujar","normal.enter":"Intro","normal.upload":"Subir","normal.default":"Predeterminado","normal.custom":"Personalizado","normal.strokeWidth":"Trazo","normal.opacity":"Opacidad",
"comment.total":"Comentario {{value}}","comment.page":"Página {{value}}","comment.status.accepted":"Aceptado","comment.status.rejected":"Rechazado","comment.status.cancelled":"Cancelado","comment.status.completed":"Completado","comment.status.none":"Ninguno","comment.status.closed":"Cerrado","comment.statusText":"Establecer estado: {{value}}",
"pdf.generationSuccess":"El archivo se ha generado y descargado correctamente",
"dateFormat.full":"{{month}}/{{day}}/{{year}} {{hour}}:{{minute}}","dateFormat.dayMonth":"{{month}}/{{day}}","dateFormat.dayMonthYear":"{{month}}/{{day}}/{{year}}",
"save.start":"Guardando...","save.success":"¡Guardado correctamente!","save.fail":"Error al guardar. {{value}}","save.noPostUrl":"{{value}} no encontrado.",
"load.fail":"Error al cargar los datos de anotación: {{value}}",
"export.fields.id":"ID","export.fields.page":"Página","export.fields.author":"Autor","export.fields.date":"Fecha","export.fields.content":"Contenido","export.fields.status":"Estado","export.fields.annotationType":"Tipo de anotación","export.fields.recordType":"Tipo","export.recordType.annotation":"Anotación","export.recordType.reply":"Respuesta",
}

T["fr"] = {
"anno":"Commentaire",
"annotations.select":"Sélectionner","annotations.highlight":"Surligner","annotations.strikeout":"Barrer","annotations.underline":"Souligner","annotations.rectangle":"Rectangle","annotations.circle":"Cercle","annotations.freehand":"Main levée","annotations.freeHighlight":"Surlignage libre","annotations.freeText":"Texte","annotations.signature":"Signature","annotations.stamp":"Tampon","annotations.note":"Note","annotations.arrow":"Flèche","annotations.cloud":"Nuage",
"toolbar.buttons.createSignature":"Créer une signature","toolbar.buttons.uploadImage":"Importer une image","toolbar.buttons.createStamp":"Créer un tampon",
"toolbar.message.selectPosition":"Veuillez choisir une position","toolbar.message.signatureArea":"Signature","toolbar.message.uploadArea":"Zone d'import","toolbar.message.uploadHint":"Cliquez pour importer ou glissez-déposez ici {{format}}, taille max {{maxSize}}",
"editor.text.startTyping":"Commencez à saisir…",
"editor.stamp.stampText":"Texte du tampon","editor.stamp.fontStyle":"Style de police","editor.stamp.fontFamily":"Police","editor.stamp.textColor":"Couleur du texte","editor.stamp.backgroundColor":"Couleur de fond","editor.stamp.borderColor":"Couleur de bordure","editor.stamp.borderStyle":"Style de bordure","editor.stamp.timestampText":"Texte d'horodatage","editor.stamp.customTimestamp":"Texte personnalisé","editor.stamp.username":"Nom d'utilisateur","editor.stamp.date":"Date","editor.stamp.time":"Heure","editor.stamp.dateFormat":"Format de date","editor.stamp.solid":"Plein","editor.stamp.dashed":"Tirets","editor.stamp.defaultText":"Brouillon",
"normal.ok":"OK","normal.cancel":"Annuler","normal.clear":"Effacer","normal.fileSizeLimit":"La taille du fichier dépasse la limite de {{value}}","normal.deleteConfirm":"Voulez-vous vraiment supprimer ?","normal.yes":"Oui","normal.no":"Non","normal.example":"p. ex. ","normal.color":"Couleur","normal.export":"Exporter","normal.save":"Enregistrer","normal.reply":"Répondre","normal.edit":"Modifier","normal.delete":"Supprimer","normal.confirm":"Confirmer","normal.unknownUser":"Utilisateur inconnu","normal.processing":"Traitement en cours, veuillez patienter...","normal.filter":"Filtrer","normal.author":"Auteur","normal.type":"Type","normal.selectAll":"Tout sélectionner","normal.more":"Plus","normal.draw":"Dessiner","normal.enter":"Entrée","normal.upload":"Importer","normal.default":"Par défaut","normal.custom":"Personnalisé","normal.strokeWidth":"Trait","normal.opacity":"Opacité",
"comment.total":"Commentaire {{value}}","comment.page":"Page {{value}}","comment.status.accepted":"Accepté","comment.status.rejected":"Rejeté","comment.status.cancelled":"Annulé","comment.status.completed":"Terminé","comment.status.none":"Aucun","comment.status.closed":"Fermé","comment.statusText":"Définir le statut : {{value}}",
"pdf.generationSuccess":"Le fichier a été généré et téléchargé avec succès",
"dateFormat.full":"{{month}}/{{day}}/{{year}} {{hour}}:{{minute}}","dateFormat.dayMonth":"{{month}}/{{day}}","dateFormat.dayMonthYear":"{{month}}/{{day}}/{{year}}",
"save.start":"Enregistrement...","save.success":"Enregistré avec succès !","save.fail":"Échec de l'enregistrement. {{value}}","save.noPostUrl":"{{value}} introuvable.",
"load.fail":"Échec du chargement des données d'annotation : {{value}}",
"export.fields.id":"ID","export.fields.page":"Page","export.fields.author":"Auteur","export.fields.date":"Date","export.fields.content":"Contenu","export.fields.status":"Statut","export.fields.annotationType":"Type d'annotation","export.fields.recordType":"Type","export.recordType.annotation":"Annotation","export.recordType.reply":"Réponse",
}

T["pt"] = {
"anno":"Comentário",
"annotations.select":"Selecionar","annotations.highlight":"Realçar","annotations.strikeout":"Tachar","annotations.underline":"Sublinhar","annotations.rectangle":"Retângulo","annotations.circle":"Círculo","annotations.freehand":"Mão livre","annotations.freeHighlight":"Realce livre","annotations.freeText":"Texto","annotations.signature":"Assinatura","annotations.stamp":"Carimbo","annotations.note":"Nota","annotations.arrow":"Seta","annotations.cloud":"Nuvem",
"toolbar.buttons.createSignature":"Criar assinatura","toolbar.buttons.uploadImage":"Enviar imagem","toolbar.buttons.createStamp":"Criar carimbo",
"toolbar.message.selectPosition":"Selecione uma posição","toolbar.message.signatureArea":"Assinatura","toolbar.message.uploadArea":"Área de envio","toolbar.message.uploadHint":"Clique para enviar ou arraste e solte aqui {{format}}, tamanho máx. {{maxSize}}",
"editor.text.startTyping":"Comece a digitar…",
"editor.stamp.stampText":"Texto do carimbo","editor.stamp.fontStyle":"Estilo da fonte","editor.stamp.fontFamily":"Fonte","editor.stamp.textColor":"Cor do texto","editor.stamp.backgroundColor":"Cor de fundo","editor.stamp.borderColor":"Cor da borda","editor.stamp.borderStyle":"Estilo da borda","editor.stamp.timestampText":"Texto de data/hora","editor.stamp.customTimestamp":"Texto personalizado","editor.stamp.username":"Nome de usuário","editor.stamp.date":"Data","editor.stamp.time":"Hora","editor.stamp.dateFormat":"Formato de data","editor.stamp.solid":"Sólido","editor.stamp.dashed":"Tracejado","editor.stamp.defaultText":"Rascunho",
"normal.ok":"OK","normal.cancel":"Cancelar","normal.clear":"Limpar","normal.fileSizeLimit":"O tamanho do arquivo excede o limite de {{value}}","normal.deleteConfirm":"Tem certeza de que deseja excluir?","normal.yes":"Sim","normal.no":"Não","normal.example":"ex. ","normal.color":"Cor","normal.export":"Exportar","normal.save":"Salvar","normal.reply":"Responder","normal.edit":"Editar","normal.delete":"Excluir","normal.confirm":"Confirmar","normal.unknownUser":"Usuário desconhecido","normal.processing":"Processando, aguarde...","normal.filter":"Filtrar","normal.author":"Autor","normal.type":"Tipo","normal.selectAll":"Selecionar tudo","normal.more":"Mais","normal.draw":"Desenhar","normal.enter":"Enter","normal.upload":"Enviar","normal.default":"Padrão","normal.custom":"Personalizado","normal.strokeWidth":"Traço","normal.opacity":"Opacidade",
"comment.total":"Comentário {{value}}","comment.page":"Página {{value}}","comment.status.accepted":"Aceito","comment.status.rejected":"Rejeitado","comment.status.cancelled":"Cancelado","comment.status.completed":"Concluído","comment.status.none":"Nenhum","comment.status.closed":"Fechado","comment.statusText":"Definir status: {{value}}",
"pdf.generationSuccess":"O arquivo foi gerado e baixado com sucesso",
"dateFormat.full":"{{month}}/{{day}}/{{year}} {{hour}}:{{minute}}","dateFormat.dayMonth":"{{month}}/{{day}}","dateFormat.dayMonthYear":"{{month}}/{{day}}/{{year}}",
"save.start":"Salvando...","save.success":"Salvo com sucesso!","save.fail":"Falha ao salvar. {{value}}","save.noPostUrl":"{{value}} não encontrado.",
"load.fail":"Falha ao carregar dados de anotação: {{value}}",
"export.fields.id":"ID","export.fields.page":"Página","export.fields.author":"Autor","export.fields.date":"Data","export.fields.content":"Conteúdo","export.fields.status":"Status","export.fields.annotationType":"Tipo de anotação","export.fields.recordType":"Tipo","export.recordType.annotation":"Anotação","export.recordType.reply":"Resposta",
}

T["it"] = {
"anno":"Commento",
"annotations.select":"Seleziona","annotations.highlight":"Evidenzia","annotations.strikeout":"Barra","annotations.underline":"Sottolinea","annotations.rectangle":"Rettangolo","annotations.circle":"Cerchio","annotations.freehand":"Mano libera","annotations.freeHighlight":"Evidenziazione libera","annotations.freeText":"Testo","annotations.signature":"Firma","annotations.stamp":"Timbro","annotations.note":"Nota","annotations.arrow":"Freccia","annotations.cloud":"Nuvola",
"toolbar.buttons.createSignature":"Crea firma","toolbar.buttons.uploadImage":"Carica immagine","toolbar.buttons.createStamp":"Crea timbro",
"toolbar.message.selectPosition":"Seleziona una posizione","toolbar.message.signatureArea":"Firma","toolbar.message.uploadArea":"Area di caricamento","toolbar.message.uploadHint":"Fai clic per caricare o trascina qui {{format}}, dimensione max {{maxSize}}",
"editor.text.startTyping":"Inizia a digitare…",
"editor.stamp.stampText":"Testo del timbro","editor.stamp.fontStyle":"Stile carattere","editor.stamp.fontFamily":"Carattere","editor.stamp.textColor":"Colore del testo","editor.stamp.backgroundColor":"Colore di sfondo","editor.stamp.borderColor":"Colore del bordo","editor.stamp.borderStyle":"Stile del bordo","editor.stamp.timestampText":"Testo data/ora","editor.stamp.customTimestamp":"Testo personalizzato","editor.stamp.username":"Nome utente","editor.stamp.date":"Data","editor.stamp.time":"Ora","editor.stamp.dateFormat":"Formato data","editor.stamp.solid":"Continuo","editor.stamp.dashed":"Tratteggiato","editor.stamp.defaultText":"Bozza",
"normal.ok":"OK","normal.cancel":"Annulla","normal.clear":"Cancella","normal.fileSizeLimit":"La dimensione del file supera il limite di {{value}}","normal.deleteConfirm":"Vuoi davvero eliminare?","normal.yes":"Sì","normal.no":"No","normal.example":"es. ","normal.color":"Colore","normal.export":"Esporta","normal.save":"Salva","normal.reply":"Rispondi","normal.edit":"Modifica","normal.delete":"Elimina","normal.confirm":"Conferma","normal.unknownUser":"Utente sconosciuto","normal.processing":"Elaborazione in corso, attendere...","normal.filter":"Filtra","normal.author":"Autore","normal.type":"Tipo","normal.selectAll":"Seleziona tutto","normal.more":"Altro","normal.draw":"Disegna","normal.enter":"Invio","normal.upload":"Carica","normal.default":"Predefinito","normal.custom":"Personalizzato","normal.strokeWidth":"Tratto","normal.opacity":"Opacità",
"comment.total":"Commento {{value}}","comment.page":"Pagina {{value}}","comment.status.accepted":"Accettato","comment.status.rejected":"Rifiutato","comment.status.cancelled":"Annullato","comment.status.completed":"Completato","comment.status.none":"Nessuno","comment.status.closed":"Chiuso","comment.statusText":"Imposta stato: {{value}}",
"pdf.generationSuccess":"Il file è stato generato e scaricato correttamente",
"dateFormat.full":"{{month}}/{{day}}/{{year}} {{hour}}:{{minute}}","dateFormat.dayMonth":"{{month}}/{{day}}","dateFormat.dayMonthYear":"{{month}}/{{day}}/{{year}}",
"save.start":"Salvataggio...","save.success":"Salvato correttamente!","save.fail":"Salvataggio non riuscito. {{value}}","save.noPostUrl":"{{value}} non trovato.",
"load.fail":"Caricamento dei dati di annotazione non riuscito: {{value}}",
"export.fields.id":"ID","export.fields.page":"Pagina","export.fields.author":"Autore","export.fields.date":"Data","export.fields.content":"Contenuto","export.fields.status":"Stato","export.fields.annotationType":"Tipo di annotazione","export.fields.recordType":"Tipo","export.recordType.annotation":"Annotazione","export.recordType.reply":"Risposta",
}

T["ja"] = {
"anno":"コメント",
"annotations.select":"選択","annotations.highlight":"ハイライト","annotations.strikeout":"取り消し線","annotations.underline":"下線","annotations.rectangle":"長方形","annotations.circle":"円","annotations.freehand":"フリーハンド","annotations.freeHighlight":"フリーハイライト","annotations.freeText":"テキスト","annotations.signature":"署名","annotations.stamp":"スタンプ","annotations.note":"注釈","annotations.arrow":"矢印","annotations.cloud":"雲形",
"toolbar.buttons.createSignature":"署名を作成","toolbar.buttons.uploadImage":"画像をアップロード","toolbar.buttons.createStamp":"スタンプを作成",
"toolbar.message.selectPosition":"位置を選択してください","toolbar.message.signatureArea":"署名","toolbar.message.uploadArea":"アップロード領域","toolbar.message.uploadHint":"クリックしてアップロード、またはここにドラッグ＆ドロップ {{format}}、最大サイズ {{maxSize}}",
"editor.text.startTyping":"入力を開始…",
"editor.stamp.stampText":"スタンプのテキスト","editor.stamp.fontStyle":"フォントスタイル","editor.stamp.fontFamily":"フォント","editor.stamp.textColor":"文字色","editor.stamp.backgroundColor":"背景色","editor.stamp.borderColor":"枠線の色","editor.stamp.borderStyle":"枠線のスタイル","editor.stamp.timestampText":"タイムスタンプのテキスト","editor.stamp.customTimestamp":"カスタムテキスト","editor.stamp.username":"ユーザー名","editor.stamp.date":"日付","editor.stamp.time":"時刻","editor.stamp.dateFormat":"日付形式","editor.stamp.solid":"実線","editor.stamp.dashed":"破線","editor.stamp.defaultText":"下書き",
"normal.ok":"OK","normal.cancel":"キャンセル","normal.clear":"クリア","normal.fileSizeLimit":"ファイルサイズが {{value}} の上限を超えています","normal.deleteConfirm":"削除してもよろしいですか？","normal.yes":"はい","normal.no":"いいえ","normal.example":"例: ","normal.color":"色","normal.export":"エクスポート","normal.save":"保存","normal.reply":"返信","normal.edit":"編集","normal.delete":"削除","normal.confirm":"確認","normal.unknownUser":"不明なユーザー","normal.processing":"処理中です。お待ちください...","normal.filter":"フィルター","normal.author":"作成者","normal.type":"種類","normal.selectAll":"すべて選択","normal.more":"その他","normal.draw":"描く","normal.enter":"確定","normal.upload":"アップロード","normal.default":"既定","normal.custom":"カスタム","normal.strokeWidth":"線の太さ","normal.opacity":"不透明度",
"comment.total":"コメント {{value}}","comment.page":"ページ {{value}}","comment.status.accepted":"承認済み","comment.status.rejected":"却下","comment.status.cancelled":"取り消し","comment.status.completed":"完了","comment.status.none":"なし","comment.status.closed":"クローズ","comment.statusText":"ステータスを設定: {{value}}",
"pdf.generationSuccess":"ファイルが正常に生成され、ダウンロードされました",
"dateFormat.full":"{{year}}/{{month}}/{{day}} {{hour}}:{{minute}}","dateFormat.dayMonth":"{{month}}/{{day}}","dateFormat.dayMonthYear":"{{year}}/{{month}}/{{day}}",
"save.start":"保存中...","save.success":"保存しました！","save.fail":"保存に失敗しました。{{value}}","save.noPostUrl":"{{value}} が見つかりません。",
"load.fail":"注釈データの読み込みに失敗しました: {{value}}",
"export.fields.id":"ID","export.fields.page":"ページ","export.fields.author":"作成者","export.fields.date":"日付","export.fields.content":"内容","export.fields.status":"ステータス","export.fields.annotationType":"注釈の種類","export.fields.recordType":"種類","export.recordType.annotation":"注釈","export.recordType.reply":"返信",
}

T["ko"] = {
"anno":"댓글",
"annotations.select":"선택","annotations.highlight":"형광펜","annotations.strikeout":"취소선","annotations.underline":"밑줄","annotations.rectangle":"사각형","annotations.circle":"원","annotations.freehand":"자유 곡선","annotations.freeHighlight":"자유 형광펜","annotations.freeText":"텍스트","annotations.signature":"서명","annotations.stamp":"스탬프","annotations.note":"메모","annotations.arrow":"화살표","annotations.cloud":"구름형",
"toolbar.buttons.createSignature":"서명 만들기","toolbar.buttons.uploadImage":"이미지 업로드","toolbar.buttons.createStamp":"스탬프 만들기",
"toolbar.message.selectPosition":"위치를 선택하세요","toolbar.message.signatureArea":"서명","toolbar.message.uploadArea":"업로드 영역","toolbar.message.uploadHint":"클릭하여 업로드하거나 여기로 끌어다 놓으세요 {{format}}, 최대 크기 {{maxSize}}",
"editor.text.startTyping":"입력을 시작하세요…",
"editor.stamp.stampText":"스탬프 텍스트","editor.stamp.fontStyle":"글꼴 스타일","editor.stamp.fontFamily":"글꼴","editor.stamp.textColor":"글자 색","editor.stamp.backgroundColor":"배경색","editor.stamp.borderColor":"테두리 색","editor.stamp.borderStyle":"테두리 스타일","editor.stamp.timestampText":"타임스탬프 텍스트","editor.stamp.customTimestamp":"사용자 지정 텍스트","editor.stamp.username":"사용자 이름","editor.stamp.date":"날짜","editor.stamp.time":"시간","editor.stamp.dateFormat":"날짜 형식","editor.stamp.solid":"실선","editor.stamp.dashed":"파선","editor.stamp.defaultText":"초안",
"normal.ok":"확인","normal.cancel":"취소","normal.clear":"지우기","normal.fileSizeLimit":"파일 크기가 {{value}} 제한을 초과합니다","normal.deleteConfirm":"정말 삭제하시겠습니까?","normal.yes":"예","normal.no":"아니요","normal.example":"예: ","normal.color":"색상","normal.export":"내보내기","normal.save":"저장","normal.reply":"답글","normal.edit":"편집","normal.delete":"삭제","normal.confirm":"확인","normal.unknownUser":"알 수 없는 사용자","normal.processing":"처리 중입니다. 잠시 기다려 주세요...","normal.filter":"필터","normal.author":"작성자","normal.type":"유형","normal.selectAll":"모두 선택","normal.more":"더 보기","normal.draw":"그리기","normal.enter":"입력","normal.upload":"업로드","normal.default":"기본값","normal.custom":"사용자 지정","normal.strokeWidth":"선 두께","normal.opacity":"불투명도",
"comment.total":"댓글 {{value}}","comment.page":"{{value}}페이지","comment.status.accepted":"수락됨","comment.status.rejected":"거부됨","comment.status.cancelled":"취소됨","comment.status.completed":"완료됨","comment.status.none":"없음","comment.status.closed":"닫힘","comment.statusText":"상태 설정: {{value}}",
"pdf.generationSuccess":"파일이 성공적으로 생성되어 다운로드되었습니다",
"dateFormat.full":"{{year}}/{{month}}/{{day}} {{hour}}:{{minute}}","dateFormat.dayMonth":"{{month}}/{{day}}","dateFormat.dayMonthYear":"{{year}}/{{month}}/{{day}}",
"save.start":"저장 중...","save.success":"저장되었습니다!","save.fail":"저장하지 못했습니다. {{value}}","save.noPostUrl":"{{value}}을(를) 찾을 수 없습니다.",
"load.fail":"주석 데이터 로드 실패: {{value}}",
"export.fields.id":"ID","export.fields.page":"페이지","export.fields.author":"작성자","export.fields.date":"날짜","export.fields.content":"내용","export.fields.status":"상태","export.fields.annotationType":"주석 유형","export.fields.recordType":"유형","export.recordType.annotation":"주석","export.recordType.reply":"답글",
}

T["ar"] = {
"anno":"تعليق",
"annotations.select":"تحديد","annotations.highlight":"تظليل","annotations.strikeout":"شطب","annotations.underline":"تسطير","annotations.rectangle":"مستطيل","annotations.circle":"دائرة","annotations.freehand":"رسم حر","annotations.freeHighlight":"تظليل حر","annotations.freeText":"نص","annotations.signature":"توقيع","annotations.stamp":"ختم","annotations.note":"ملاحظة","annotations.arrow":"سهم","annotations.cloud":"سحابة",
"toolbar.buttons.createSignature":"إنشاء توقيع","toolbar.buttons.uploadImage":"رفع صورة","toolbar.buttons.createStamp":"إنشاء ختم",
"toolbar.message.selectPosition":"يرجى تحديد موضع","toolbar.message.signatureArea":"توقيع","toolbar.message.uploadArea":"منطقة الرفع","toolbar.message.uploadHint":"انقر للرفع أو اسحب وأفلت هنا {{format}}، الحجم الأقصى {{maxSize}}",
"editor.text.startTyping":"ابدأ الكتابة…",
"editor.stamp.stampText":"نص الختم","editor.stamp.fontStyle":"نمط الخط","editor.stamp.fontFamily":"الخط","editor.stamp.textColor":"لون النص","editor.stamp.backgroundColor":"لون الخلفية","editor.stamp.borderColor":"لون الحد","editor.stamp.borderStyle":"نمط الحد","editor.stamp.timestampText":"نص الطابع الزمني","editor.stamp.customTimestamp":"نص مخصص","editor.stamp.username":"اسم المستخدم","editor.stamp.date":"التاريخ","editor.stamp.time":"الوقت","editor.stamp.dateFormat":"تنسيق التاريخ","editor.stamp.solid":"متصل","editor.stamp.dashed":"متقطع","editor.stamp.defaultText":"مسودة",
"normal.ok":"موافق","normal.cancel":"إلغاء","normal.clear":"مسح","normal.fileSizeLimit":"حجم الملف يتجاوز الحد {{value}}","normal.deleteConfirm":"هل أنت متأكد أنك تريد الحذف؟","normal.yes":"نعم","normal.no":"لا","normal.example":"مثال: ","normal.color":"اللون","normal.export":"تصدير","normal.save":"حفظ","normal.reply":"رد","normal.edit":"تعديل","normal.delete":"حذف","normal.confirm":"تأكيد","normal.unknownUser":"مستخدم غير معروف","normal.processing":"جارٍ المعالجة، يرجى الانتظار...","normal.filter":"تصفية","normal.author":"المؤلف","normal.type":"النوع","normal.selectAll":"تحديد الكل","normal.more":"المزيد","normal.draw":"رسم","normal.enter":"إدخال","normal.upload":"رفع","normal.default":"افتراضي","normal.custom":"مخصص","normal.strokeWidth":"سمك الخط","normal.opacity":"الشفافية",
"comment.total":"تعليق {{value}}","comment.page":"صفحة {{value}}","comment.status.accepted":"مقبول","comment.status.rejected":"مرفوض","comment.status.cancelled":"ملغى","comment.status.completed":"مكتمل","comment.status.none":"لا شيء","comment.status.closed":"مغلق","comment.statusText":"تعيين الحالة: {{value}}",
"pdf.generationSuccess":"تم إنشاء الملف وتنزيله بنجاح",
"dateFormat.full":"{{year}}/{{month}}/{{day}} {{hour}}:{{minute}}","dateFormat.dayMonth":"{{day}}/{{month}}","dateFormat.dayMonthYear":"{{day}}/{{month}}/{{year}}",
"save.start":"جارٍ الحفظ...","save.success":"تم الحفظ بنجاح!","save.fail":"فشل الحفظ. {{value}}","save.noPostUrl":"{{value}} غير موجود.",
"load.fail":"فشل تحميل بيانات التعليقات التوضيحية: {{value}}",
"export.fields.id":"المعرف","export.fields.page":"الصفحة","export.fields.author":"المؤلف","export.fields.date":"التاريخ","export.fields.content":"المحتوى","export.fields.status":"الحالة","export.fields.annotationType":"نوع التعليق التوضيحي","export.fields.recordType":"النوع","export.recordType.annotation":"تعليق توضيحي","export.recordType.reply":"رد",
}

T["vi"] = {
"anno":"Bình luận",
"annotations.select":"Chọn","annotations.highlight":"Tô sáng","annotations.strikeout":"Gạch ngang","annotations.underline":"Gạch chân","annotations.rectangle":"Hình chữ nhật","annotations.circle":"Hình tròn","annotations.freehand":"Vẽ tự do","annotations.freeHighlight":"Tô sáng tự do","annotations.freeText":"Văn bản","annotations.signature":"Chữ ký","annotations.stamp":"Con dấu","annotations.note":"Ghi chú","annotations.arrow":"Mũi tên","annotations.cloud":"Đám mây",
"toolbar.buttons.createSignature":"Tạo chữ ký","toolbar.buttons.uploadImage":"Tải ảnh lên","toolbar.buttons.createStamp":"Tạo con dấu",
"toolbar.message.selectPosition":"Vui lòng chọn vị trí","toolbar.message.signatureArea":"Chữ ký","toolbar.message.uploadArea":"Khu vực tải lên","toolbar.message.uploadHint":"Nhấp để tải lên hoặc kéo và thả vào đây {{format}}, dung lượng tối đa {{maxSize}}",
"editor.text.startTyping":"Bắt đầu nhập…",
"editor.stamp.stampText":"Văn bản con dấu","editor.stamp.fontStyle":"Kiểu phông chữ","editor.stamp.fontFamily":"Phông chữ","editor.stamp.textColor":"Màu chữ","editor.stamp.backgroundColor":"Màu nền","editor.stamp.borderColor":"Màu viền","editor.stamp.borderStyle":"Kiểu viền","editor.stamp.timestampText":"Văn bản dấu thời gian","editor.stamp.customTimestamp":"Văn bản tùy chỉnh","editor.stamp.username":"Tên người dùng","editor.stamp.date":"Ngày","editor.stamp.time":"Giờ","editor.stamp.dateFormat":"Định dạng ngày","editor.stamp.solid":"Liền nét","editor.stamp.dashed":"Nét đứt","editor.stamp.defaultText":"Bản nháp",
"normal.ok":"OK","normal.cancel":"Hủy","normal.clear":"Xóa","normal.fileSizeLimit":"Kích thước tệp vượt quá giới hạn {{value}}","normal.deleteConfirm":"Bạn có chắc chắn muốn xóa không?","normal.yes":"Có","normal.no":"Không","normal.example":"ví dụ: ","normal.color":"Màu","normal.export":"Xuất","normal.save":"Lưu","normal.reply":"Trả lời","normal.edit":"Sửa","normal.delete":"Xóa","normal.confirm":"Xác nhận","normal.unknownUser":"Người dùng không xác định","normal.processing":"Đang xử lý, vui lòng đợi...","normal.filter":"Lọc","normal.author":"Tác giả","normal.type":"Loại","normal.selectAll":"Chọn tất cả","normal.more":"Thêm","normal.draw":"Vẽ","normal.enter":"Nhập","normal.upload":"Tải lên","normal.default":"Mặc định","normal.custom":"Tùy chỉnh","normal.strokeWidth":"Độ dày nét","normal.opacity":"Độ mờ",
"comment.total":"Bình luận {{value}}","comment.page":"Trang {{value}}","comment.status.accepted":"Đã chấp nhận","comment.status.rejected":"Đã từ chối","comment.status.cancelled":"Đã hủy","comment.status.completed":"Đã hoàn thành","comment.status.none":"Không có","comment.status.closed":"Đã đóng","comment.statusText":"Đặt trạng thái: {{value}}",
"pdf.generationSuccess":"Tệp đã được tạo và tải xuống thành công",
"dateFormat.full":"{{day}}/{{month}}/{{year}} {{hour}}:{{minute}}","dateFormat.dayMonth":"{{day}}/{{month}}","dateFormat.dayMonthYear":"{{day}}/{{month}}/{{year}}",
"save.start":"Đang lưu...","save.success":"Đã lưu thành công!","save.fail":"Lưu không thành công. {{value}}","save.noPostUrl":"Không tìm thấy {{value}}.",
"load.fail":"Tải dữ liệu chú thích không thành công: {{value}}",
"export.fields.id":"ID","export.fields.page":"Trang","export.fields.author":"Tác giả","export.fields.date":"Ngày","export.fields.content":"Nội dung","export.fields.status":"Trạng thái","export.fields.annotationType":"Loại chú thích","export.fields.recordType":"Loại","export.recordType.annotation":"Chú thích","export.recordType.reply":"Trả lời",
}

T["id"] = {
"anno":"Komentar",
"annotations.select":"Pilih","annotations.highlight":"Sorot","annotations.strikeout":"Coret","annotations.underline":"Garis bawah","annotations.rectangle":"Persegi panjang","annotations.circle":"Lingkaran","annotations.freehand":"Gambar bebas","annotations.freeHighlight":"Sorot bebas","annotations.freeText":"Teks","annotations.signature":"Tanda tangan","annotations.stamp":"Stempel","annotations.note":"Catatan","annotations.arrow":"Panah","annotations.cloud":"Awan",
"toolbar.buttons.createSignature":"Buat tanda tangan","toolbar.buttons.uploadImage":"Unggah gambar","toolbar.buttons.createStamp":"Buat stempel",
"toolbar.message.selectPosition":"Silakan pilih posisi","toolbar.message.signatureArea":"Tanda tangan","toolbar.message.uploadArea":"Area unggah","toolbar.message.uploadHint":"Klik untuk mengunggah atau seret dan lepas ke sini {{format}}, ukuran maks {{maxSize}}",
"editor.text.startTyping":"Mulai mengetik…",
"editor.stamp.stampText":"Teks stempel","editor.stamp.fontStyle":"Gaya font","editor.stamp.fontFamily":"Font","editor.stamp.textColor":"Warna teks","editor.stamp.backgroundColor":"Warna latar","editor.stamp.borderColor":"Warna batas","editor.stamp.borderStyle":"Gaya batas","editor.stamp.timestampText":"Teks stempel waktu","editor.stamp.customTimestamp":"Teks kustom","editor.stamp.username":"Nama pengguna","editor.stamp.date":"Tanggal","editor.stamp.time":"Waktu","editor.stamp.dateFormat":"Format tanggal","editor.stamp.solid":"Padat","editor.stamp.dashed":"Putus-putus","editor.stamp.defaultText":"Draf",
"normal.ok":"OK","normal.cancel":"Batal","normal.clear":"Hapus","normal.fileSizeLimit":"Ukuran file melebihi batas {{value}}","normal.deleteConfirm":"Apakah Anda yakin ingin menghapus?","normal.yes":"Ya","normal.no":"Tidak","normal.example":"mis. ","normal.color":"Warna","normal.export":"Ekspor","normal.save":"Simpan","normal.reply":"Balas","normal.edit":"Edit","normal.delete":"Hapus","normal.confirm":"Konfirmasi","normal.unknownUser":"Pengguna tidak dikenal","normal.processing":"Memproses, harap tunggu...","normal.filter":"Filter","normal.author":"Penulis","normal.type":"Tipe","normal.selectAll":"Pilih semua","normal.more":"Lainnya","normal.draw":"Gambar","normal.enter":"Enter","normal.upload":"Unggah","normal.default":"Default","normal.custom":"Kustom","normal.strokeWidth":"Tebal garis","normal.opacity":"Opasitas",
"comment.total":"Komentar {{value}}","comment.page":"Halaman {{value}}","comment.status.accepted":"Diterima","comment.status.rejected":"Ditolak","comment.status.cancelled":"Dibatalkan","comment.status.completed":"Selesai","comment.status.none":"Tidak ada","comment.status.closed":"Ditutup","comment.statusText":"Atur status: {{value}}",
"pdf.generationSuccess":"File berhasil dibuat dan diunduh",
"dateFormat.full":"{{day}}/{{month}}/{{year}} {{hour}}:{{minute}}","dateFormat.dayMonth":"{{day}}/{{month}}","dateFormat.dayMonthYear":"{{day}}/{{month}}/{{year}}",
"save.start":"Menyimpan...","save.success":"Berhasil disimpan!","save.fail":"Gagal menyimpan. {{value}}","save.noPostUrl":"{{value}} tidak ditemukan.",
"load.fail":"Gagal memuat data anotasi: {{value}}",
"export.fields.id":"ID","export.fields.page":"Halaman","export.fields.author":"Penulis","export.fields.date":"Tanggal","export.fields.content":"Konten","export.fields.status":"Status","export.fields.annotationType":"Tipe anotasi","export.fields.recordType":"Tipe","export.recordType.annotation":"Anotasi","export.recordType.reply":"Balasan",
}

T["ro"] = {
"anno":"Comentariu",
"annotations.select":"Selectare","annotations.highlight":"Evidențiere","annotations.strikeout":"Tăiere","annotations.underline":"Subliniere","annotations.rectangle":"Dreptunghi","annotations.circle":"Cerc","annotations.freehand":"Mână liberă","annotations.freeHighlight":"Evidențiere liberă","annotations.freeText":"Text","annotations.signature":"Semnătură","annotations.stamp":"Ștampilă","annotations.note":"Notă","annotations.arrow":"Săgeată","annotations.cloud":"Nor",
"toolbar.buttons.createSignature":"Creează semnătură","toolbar.buttons.uploadImage":"Încarcă imagine","toolbar.buttons.createStamp":"Creează ștampilă",
"toolbar.message.selectPosition":"Selectați o poziție","toolbar.message.signatureArea":"Semnătură","toolbar.message.uploadArea":"Zonă de încărcare","toolbar.message.uploadHint":"Faceți clic pentru a încărca sau trageți și plasați aici {{format}}, dimensiune max {{maxSize}}",
"editor.text.startTyping":"Începeți să scrieți…",
"editor.stamp.stampText":"Text ștampilă","editor.stamp.fontStyle":"Stil font","editor.stamp.fontFamily":"Font","editor.stamp.textColor":"Culoare text","editor.stamp.backgroundColor":"Culoare fundal","editor.stamp.borderColor":"Culoare bordură","editor.stamp.borderStyle":"Stil bordură","editor.stamp.timestampText":"Text marcaj temporal","editor.stamp.customTimestamp":"Text personalizat","editor.stamp.username":"Nume utilizator","editor.stamp.date":"Dată","editor.stamp.time":"Oră","editor.stamp.dateFormat":"Format dată","editor.stamp.solid":"Continuu","editor.stamp.dashed":"Întrerupt","editor.stamp.defaultText":"Ciornă",
"normal.ok":"OK","normal.cancel":"Anulare","normal.clear":"Ștergere","normal.fileSizeLimit":"Dimensiunea fișierului depășește limita de {{value}}","normal.deleteConfirm":"Sigur doriți să ștergeți?","normal.yes":"Da","normal.no":"Nu","normal.example":"de ex. ","normal.color":"Culoare","normal.export":"Export","normal.save":"Salvare","normal.reply":"Răspuns","normal.edit":"Editare","normal.delete":"Ștergere","normal.confirm":"Confirmare","normal.unknownUser":"Utilizator necunoscut","normal.processing":"Se procesează, vă rugăm așteptați...","normal.filter":"Filtrare","normal.author":"Autor","normal.type":"Tip","normal.selectAll":"Selectează tot","normal.more":"Mai mult","normal.draw":"Desenare","normal.enter":"Enter","normal.upload":"Încărcare","normal.default":"Implicit","normal.custom":"Personalizat","normal.strokeWidth":"Grosime linie","normal.opacity":"Opacitate",
"comment.total":"Comentariu {{value}}","comment.page":"Pagina {{value}}","comment.status.accepted":"Acceptat","comment.status.rejected":"Respins","comment.status.cancelled":"Anulat","comment.status.completed":"Finalizat","comment.status.none":"Niciunul","comment.status.closed":"Închis","comment.statusText":"Setați starea: {{value}}",
"pdf.generationSuccess":"Fișierul a fost generat și descărcat cu succes",
"dateFormat.full":"{{day}}/{{month}}/{{year}} {{hour}}:{{minute}}","dateFormat.dayMonth":"{{day}}/{{month}}","dateFormat.dayMonthYear":"{{day}}/{{month}}/{{year}}",
"save.start":"Se salvează...","save.success":"Salvat cu succes!","save.fail":"Salvarea a eșuat. {{value}}","save.noPostUrl":"{{value}} nu a fost găsit.",
"load.fail":"Încărcarea datelor de adnotare a eșuat: {{value}}",
"export.fields.id":"ID","export.fields.page":"Pagină","export.fields.author":"Autor","export.fields.date":"Dată","export.fields.content":"Conținut","export.fields.status":"Stare","export.fields.annotationType":"Tip adnotare","export.fields.recordType":"Tip","export.recordType.annotation":"Adnotare","export.recordType.reply":"Răspuns",
}

T["zh-TW"] = {
"anno":"批註",
"annotations.select":"選擇","annotations.highlight":"螢光標示","annotations.strikeout":"刪除線","annotations.underline":"底線","annotations.rectangle":"矩形","annotations.circle":"圓形","annotations.freehand":"手繪","annotations.freeHighlight":"自由標示","annotations.freeText":"文字","annotations.signature":"簽名","annotations.stamp":"蓋章","annotations.note":"註解","annotations.arrow":"箭頭","annotations.cloud":"雲形",
"toolbar.buttons.createSignature":"建立簽名","toolbar.buttons.uploadImage":"上傳圖片","toolbar.buttons.createStamp":"建立印章",
"toolbar.message.selectPosition":"請選擇位置","toolbar.message.signatureArea":"簽名","toolbar.message.uploadArea":"上傳區域","toolbar.message.uploadHint":"點擊上傳或拖放至此 {{format}}，檔案大小上限 {{maxSize}}",
"editor.text.startTyping":"開始輸入…",
"editor.stamp.stampText":"印章文字","editor.stamp.fontStyle":"字型樣式","editor.stamp.fontFamily":"字型","editor.stamp.textColor":"文字色彩","editor.stamp.backgroundColor":"背景色彩","editor.stamp.borderColor":"邊框色彩","editor.stamp.borderStyle":"邊框樣式","editor.stamp.timestampText":"時間戳記文字","editor.stamp.customTimestamp":"自訂文字","editor.stamp.username":"使用者名稱","editor.stamp.date":"日期","editor.stamp.time":"時間","editor.stamp.dateFormat":"日期格式","editor.stamp.solid":"實線","editor.stamp.dashed":"虛線","editor.stamp.defaultText":"草稿",
"normal.ok":"確定","normal.cancel":"取消","normal.clear":"清除","normal.fileSizeLimit":"檔案大小超過 {{value}} 上限","normal.deleteConfirm":"確定要刪除嗎？","normal.yes":"是","normal.no":"否","normal.example":"例如：","normal.color":"色彩","normal.export":"匯出","normal.save":"儲存","normal.reply":"回覆","normal.edit":"編輯","normal.delete":"刪除","normal.confirm":"確認","normal.unknownUser":"不明使用者","normal.processing":"處理中，請稍候...","normal.filter":"篩選","normal.author":"作者","normal.type":"類型","normal.selectAll":"全選","normal.more":"更多","normal.draw":"繪製","normal.enter":"輸入","normal.upload":"上傳","normal.default":"預設","normal.custom":"自訂","normal.strokeWidth":"線條粗細","normal.opacity":"不透明度",
"comment.total":"註解 {{value}}","comment.page":"第 {{value}} 頁","comment.status.accepted":"已接受","comment.status.rejected":"已拒絕","comment.status.cancelled":"已取消","comment.status.completed":"已完成","comment.status.none":"無","comment.status.closed":"已關閉","comment.statusText":"設定狀態：{{value}}",
"pdf.generationSuccess":"檔案已成功產生並下載",
"dateFormat.full":"{{year}}/{{month}}/{{day}} {{hour}}:{{minute}}","dateFormat.dayMonth":"{{month}}/{{day}}","dateFormat.dayMonthYear":"{{year}}/{{month}}/{{day}}",
"save.start":"儲存中...","save.success":"儲存成功！","save.fail":"儲存失敗。{{value}}","save.noPostUrl":"找不到 {{value}}。",
"load.fail":"註解資料載入失敗：{{value}}",
"export.fields.id":"ID","export.fields.page":"頁","export.fields.author":"作者","export.fields.date":"日期","export.fields.content":"內容","export.fields.status":"狀態","export.fields.annotationType":"註解類型","export.fields.recordType":"類型","export.recordType.annotation":"註解","export.recordType.reply":"回覆",
}

# ---- build nested dict per lang, mirroring EN exactly ----
import re as _re
PH = _re.compile(r"\{\{[^}]+\}\}")

def flat_keys(o, p=""):
    out = {}
    for k, v in o.items():
        nk = f"{p}{k}"
        if isinstance(v, dict): out.update(flat_keys(v, nk + "."))
        else: out[nk] = v
    return out

EN_FLAT = flat_keys(EN)

def nest(flat):
    root = {}
    for dk, val in flat.items():
        parts = dk.split(".")
        cur = root
        for seg in parts[:-1]:
            cur = cur.setdefault(seg, {})
        cur[parts[-1]] = val
    return root

errors = []
built = {}
for lang, flat in T.items():
    # key parity
    missing = set(EN_FLAT) - set(flat)
    extra = set(flat) - set(EN_FLAT)
    if missing: errors.append(f"{lang}: MISSING {sorted(missing)}")
    if extra: errors.append(f"{lang}: EXTRA {sorted(extra)}")
    # placeholder parity
    for k in set(EN_FLAT) & set(flat):
        en_ph = sorted(PH.findall(EN_FLAT[k]))
        tr_ph = sorted(PH.findall(flat[k]))
        if en_ph != tr_ph:
            errors.append(f"{lang}.{k}: placeholder mismatch en={en_ph} tr={tr_ph}")
    built[lang] = nest(flat)

if errors:
    print("VALIDATION ERRORS:")
    print("\n".join(errors))
    sys.exit(1)

print(f"All {len(built)} languages validated: {sorted(built)} — each 96 leaves, placeholders OK")

# ---- generate insertion + patch bundle ----
src = open(BUNDLE, encoding="utf-8").read()
anchor = "Oe={"
assert src.count(anchor) == 1, f"anchor count = {src.count(anchor)} (expected 1)"

def js_entry(lang, nested):
    j = json.dumps(nested, ensure_ascii=False, separators=(",", ":"))
    body = j.replace("\\", "\\\\").replace("'", "\\'")
    key = lang if _re.fullmatch(r"[A-Za-z]+", lang) else f'"{lang}"'
    return f"{key}:{{translation:JSON.parse('{body}')}}"

# preserve a stable order
order = ["ar","es","fr","id","it","ja","ko","pt","ro","vi","zh-TW"]
entries = ",".join(js_entry(l, built[l]) for l in order) + ","
new_src = src.replace(anchor, anchor + entries, 1)

# Region codes (len>2) resolve through the Ae table, NOT i18next's own fallback.
# Map the region codes we actually send: es-ES->es, pt-BR->pt, zh-TW->zh-TW.
# (i18next formats lng "zh-tw" -> "zh-TW", so the Oe key + Ae value are "zh-TW".)
AE_OLD = 'Ae={"zh-cn":"zh","en-us":"en","de-de":"de"}'
AE_NEW = 'Ae={"zh-cn":"zh","en-us":"en","de-de":"de","es-es":"es","pt-br":"pt","zh-tw":"zh-TW"}'
assert new_src.count(AE_OLD) == 1, f"Ae anchor count = {new_src.count(AE_OLD)}"
new_src = new_src.replace(AE_OLD, AE_NEW, 1)

# sanity: bundle still parses-ish — check our inserted JSON.parse strings are balanced by re-extracting
for l in order:
    key = l if _re.fullmatch(r"[A-Za-z]+", l) else f'"{l}"'
    pat = _re.escape(key) + r":\{translation:JSON\.parse\('(.+?)'\)\}"
    m = _re.search(pat, new_src, _re.S)
    assert m, f"re-extract failed for {l}"
    # unescape JS-string back to JSON then json.loads
    js_str = m.group(1)
    json_text = js_str.replace("\\'", "'").replace("\\\\", "\\")
    obj = json.loads(json_text)
    assert flat_keys(obj).keys() == EN_FLAT.keys(), f"{l} key parity after round-trip failed"

open(BUNDLE, "w", encoding="utf-8").write(new_src)
print(f"Patched bundle: +{len(order)} languages, +{len(new_src)-len(src)} bytes")
