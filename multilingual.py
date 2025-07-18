m3_symbol_by_lang = {
    'afrikaans':'af',
    'chinese': 'zh',
    'english': 'en',
    'italian': 'it',
    'javanese': 'jv',
    'portuguese': 'pt',
    'swahili': 'sw',
    'thai': 'th',
    'vietnamese': 'vi'
}

m3_base_prompt = {
    'en': "The following is a multiple-choice question.",
    'zh': "以下是一道选择题。",
    'it': "La seguente è una domanda a scelta multipla.",
    'pt': "A seguir está uma pergunta de múltipla escolha.",
    'vi': "Dưới đây là một câu hỏi trắc nghiệm.",
    'th': "ต่อไปนี้เป็นคำถามแบบปรนัย",
    'sw': "Ifuatayo ni swali la chaguo nyingi.",
    'af': "Die volgende is 'n meerkeusevraag.",
    'jv': "Ing ngisor iki minangka pitakon pilihan ganda."
}

m3_cot_prompt_by_symbol = {
    'en': "Let's think step-by-step in English.",
    'zh': "让我们用中文一步步思考。",
    'it': "Pensiamo passo dopo passo in italiano.",
    'pt': "Vamos pensar passo a passo em português.",
    'vi': "Hãy suy nghĩ từng bước bằng tiếng Việt.",
    'th': "มาคิดทีละขั้นตอนในภาษาไทย.",
    'sw': "Wacha tufikiri hatua kwa hatua kwa Kiswahili.",
    'af': "Kom ons dink stap-vir-stap in Afrikaans.",
    'jv': "Ayo mikir kanthi bertahap nganggo basa Jawa."
}

m3_answer_prompt = {
    'en': "You should provide the final answer at the end in the format: 'Answer: [option]'",
    'zh': "你应该在最后提供最终答案，格式如下：'答案: [选项]'",
    'it': "Dovresti fornire la risposta finale alla fine nel formato: 'Risposta: [opzione]'",
    'pt': "Você deve fornecer a resposta final no final no formato: 'Resposta: [opção]'",
    'vi': "Bạn nên cung cấp câu trả lời cuối cùng ở cuối theo định dạng: 'Đáp án: [lựa chọn]'",
    'th': "คุณควรให้คำตอบสุดท้ายที่ท้ายในรูปแบบ: 'คำตอบ: [ตัวเลือก]'",
    'sw': "Unapaswa kutoa jibu la mwisho mwishoni kwa muundo: 'Jibu: [chaguo]'",
    'af': "Jy moet die finale antwoord aan die einde verskaf in die formaat: 'Antwoord: [opsie]'",
    'jv': "Sampeyan kudu nyedhiyakake jawaban pungkasan ing pungkasan nganggo format: 'Wangsulan: [pilihan]'"
}

dataset_lang_mapping = {
    "M3Exam": { 
        "lang_by_symbol": {
            'af': 'afrikaans',
            'zh': 'chinese',
            'en': 'english',
            'it': 'italian',
            'jv': 'javanese',
            'pt': 'portuguese',
            'sw': 'swahili',
            'th': 'thai',
            'vi': 'vietnamese'
        }, 
        "symbol_by_lang": {
            'afrikaans':'af',
            'chinese': 'zh',
            'english': 'en',
            'italian': 'it',
            'javanese': 'jv',
            'portuguese': 'pt',
            'swahili': 'sw',
            'thai': 'th',
            'vietnamese': 'vi'
        },
        "base_prompt": {
            "en": "The following is a multiple-choice question.",
            "zh": "以下是一道选择题。",
            "it": "La seguente è una domanda a scelta multipla.",
            "pt": "A seguir está uma pergunta de múltipla escolha.",
            "vi": "Dưới đây là một câu hỏi trắc nghiệm.",
            "th": "ต่อไปนี้เป็นคำถามแบบปรนัย",
            "sw": "Ifuatayo ni swali la chaguo nyingi.",
            "af": "Die volgende is 'n meerkeusevraag.",
            "jv": "Ing ngisor iki minangka pitakon pilihan ganda."
        },
        "answer_prompt": {
            'en': "You should provide the final answer at the end in the format: 'Answer: [option]'",
            'zh': "你应该在最后提供最终答案，格式如下：'答案: [选项]'",
            'it': "Dovresti fornire la risposta finale alla fine nel formato: 'Risposta: [opzione]'",
            'pt': "Você deve fornecer a resposta final no final no formato: 'Resposta: [opção]'",
            'vi': "Bạn nên cung cấp câu trả lời cuối cùng ở cuối theo định dạng: 'Đáp án: [lựa chọn]'",
            'th': "คุณควรให้คำตอบสุดท้ายที่ท้ายในรูปแบบ: 'คำตอบ: [ตัวเลือก]'",
            'sw': "Unapaswa kutoa jibu la mwisho mwishoni kwa muundo: 'Jibu: [chaguo]'",
            'af': "Jy moet die finale antwoord aan die einde verskaf in die formaat: 'Antwoord: [opsie]'",
            'jv': "Sampeyan kudu nyedhiyakake jawaban pungkasan ing pungkasan nganggo format: 'Wangsulan: [pilihan]'"

        },
        "cot_prompt":{
            'en': "Let's think step-by-step in English, and provide the final answer at the end in the format: 'Answer: [option]'",
            'zh': "让我们用中文一步步思考，并在最后以以下格式提供答案：'答案: [选项]'",
            'it': "Pensiamo passo dopo passo in italiano e forniamo la risposta finale alla fine nel formato: 'Risposta: [opzione]'",
            'pt': "Vamos pensar passo a passo em português e fornecer a resposta final no final no formato: 'Resposta: [opção]'",
            'vi': "Hãy suy nghĩ từng bước bằng tiếng Việt và cung cấp câu trả lời cuối cùng ở cuối theo định dạng: 'Đáp án: [lựa chọn]'",
            'th': "มาคิดทีละขั้นตอนในภาษาไทย และให้คำตอบสุดท้ายในตอนท้ายในรูปแบบ: 'คำตอบ: [ตัวเลือก]'",
            'sw': "Wacha tufikiri hatua kwa hatua kwa Kiswahili, na toa jibu la mwisho mwishoni kwa muundo: 'Jibu: [chaguo]'",
            'af': "Kom ons dink stap-vir-stap in Afrikaans, en gee die finale antwoord aan die einde in die formaat: 'Antwoord: [opsie]'",
            'jv': "Ayo mikir kanthi bertahap nganggo basa Jawa, lan weneh jawaban pungkasan ing pungkasan kanthi format: 'Jawaban: [pilihan]'"
        }
    },
    "MKQA": {
        "lang_by_symbol": {
            'de': 'german',
            'en': 'english',
            'es': 'spanish',
            'fr': 'french',
            'ja': 'japanese',
            'ru': 'russian',
            'th': 'thai',
            'tr': 'turkish',
            'vi': 'vietnamese',
            'zh_cn': 'chinese',
        }, 
        "symbol_by_lang": {
            'german': 'de',
            'english': 'en',
            'spanish': 'es',
            'french': 'fr',
            'japanese': 'ja',
            'russian': 'ru',
            'thai': 'th',
            'turkish': 'tr',
            'vietnamese': 'vi',
            'chinese': 'zh_cn',
        },
        "base_prompt": {
            'en': 'Answer the question in one or a few words in English: ',
            'de': 'Beantworte die Frage mit einem oder wenigen Worten auf Deutsch: ',
            'es': 'Responde a la pregunta en una o pocas palabras en español: ',
            'fr': 'Répondez à la question en un ou quelques mots en français: ',
            'ja': '質問に日本語で一言または数語で答えてください: ',
            'ru': 'Ответьте на вопрос одним или несколькими словами на русском: ',
            'th': 'ตอบคำถามเป็นภาษาไทยสั้น ๆ หรือไม่กี่คำ: ',
            'tr': 'Soruyu Türkçe olarak bir veya birkaç kelimeyle yanıtlayın: ',
            'vi': 'Trả lời câu hỏi bằng một hoặc vài từ bằng tiếng Việt: ',
            'zh_cn': '请用中文用一两个词回答问题：'
        },
        "answer_prompt": {
            "en": "You should provide the final answer at the end in the format: 'Answer: [one or a few words]'.",
            "de": "Sie sollten die endgültige Antwort am Ende im folgenden Format angeben: 'Antwort: [ein oder wenige Wörter]'.",
            "es": "Debes proporcionar la respuesta final al final en el formato: 'Respuesta: [una o pocas palabras]'.",
            "fr": "Vous devez fournir la réponse finale à la fin dans le format : 'Réponse : [un ou quelques mots]'.",
            "ja": "最終的な回答は最後に次の形式で記載してください: '回答: [1語または数語]'.",
            "ru": "Вы должны указать окончательный ответ в конце в следующем формате: 'Ответ: [одно или несколько слов]'.",
            "th": "คุณควรให้คำตอบสุดท้ายที่ส่วนท้ายในรูปแบบ: 'คำตอบ: [หนึ่งคำหรือสองสามคำ]'.",
            "tr": "Nihai yanıtınızı sonunda şu formatta vermelisiniz: 'Cevap: [bir veya birkaç kelime]'.",
            "vi": "Bạn nên đưa ra câu trả lời cuối cùng ở cuối theo định dạng: 'Trả lời: [một hoặc vài từ]'.",
            "zh_cn": "你应该在最后提供最终答案，格式如下：'回答: [一个或几个词]'."
        },
        "binary_prompt": {
            'en': 'Answer should be either "yes" or "no".',
            'de': 'Die Antwort sollte entweder "yes" oder "no" sein.',
            'es': 'La respuesta debe ser "yes" o "no".',
            'fr': 'La réponse doit être soit "yes" soit "no".',
            'ja': '回答は "yes" または "no" のいずれかである必要があります。',
            'ru': 'Ответ должен быть либо "yes", либо "no".',
            'th': 'คำตอบควรเป็น "yes" หรือ "no".',
            'tr': 'Yanıt "yes" veya "no" olmalıdır.',
            'vi': 'Câu trả lời phải là "yes" hoặc "no".',
            'zh_cn': '答案应为 "yes" 或 "no"。'
        },
        "cot_prompt":{
            "en": "Let's think step-by-step in English.",
            "de": "Lass uns Schritt für Schritt auf Deutsch nachdenken.",
            "es": "Pensemos paso a paso en español.",
            "fr": "Réfléchissons étape par étape en français.",
            "ja": "日本語で一歩ずつ考えましょう。",
            "ru": "Давайте подумаем шаг за шагом на русском.",
            "th": "ลองคิดทีละขั้นตอนเป็นภาษาไทย",
            "tr": "Haydi adım adım Türkçe düşünelim.",
            "vi": "Hãy suy nghĩ từng bước một bằng tiếng Việt.",
            "zh_cn": "让我们用中文一步步思考。"
        }
    },
    "XCOPA": {
        "lang_by_symbol": {
            'et': 'estonian',
            'ht': 'haitian creole',
            'id': 'indonesian',
            'it': 'italian',
            'qu': 'quechua',
            'sw': 'swahili',
            'ta': 'tamil',
            'th': 'thai',
            'tr': 'turkish',
            'vi': 'vietnamese',
            'zh': 'chinese'

        }, 
        "symbol_by_lang": {
            'estonian': 'et',
            'haitian creole': 'ht',
            'indonesian': 'id',
            'italian': 'it',
            'quechua': 'qu',
            'swahili': 'sw',
            'tamil': 'ta',
            'thai': 'th',
            'turkish': 'tr',
            'vietnamese': 'vi',
            'chinese': 'zh'
        },
        "base_prompt": {
            'en': 'Here is a premise: [premise]. What is the [question]? Help me pick the more plausible option: -choice1: [choice1], -choice2: [choice]',
            'et': "Siin on eeltingimus: [premise]. Mis on [question]? Aita mul valida usutavam variant: -valik1: [choice1], -valik2: [choice2]",
            'ht': "Men yon premis: [premise]. Ki sa ki [question]? Ede m chwazi opsyon ki pi plizib: -chwa1: [choice1], -chwa2: [choice2]",
            'id': "Berikut adalah premis: [premise]. Apa itu [question]? Bantu saya memilih opsi yang lebih masuk akal: -pilihan1: [choice1], -pilihan2: [choice2]",
            'it': "Ecco una premessa: [premise]. Qual è la [question]? Aiutami a scegliere l'opzione più plausibile: -scelta1: [choice1], -scelta2: [choice2]",
            'qu': "Kaymi huk ñawpaq rimaymi: [premise]. Ima [question]? Yanapaway ima kichkanku akllayta: -akllay1: [choice1], -akllay2: [choice2]",
            'sw': "Hii hapa ni dhana: [premise]. Je, ni nini [question]? Nisaidie kuchagua chaguo linaloonekana linawezekana zaidi: -chaguo1: [choice1], -chaguo2: [choice2]",
            'ta': "இங்கே ஒரு முன்னுரை: [premise]. என்ன [question]? மிகவும் நேர்மறையான விருப்பத்தை தேர்ந்தெடுக்க எனக்கு உதவுங்கள்: -விருப்பு1: [choice1], -விருப்பு2: [choice2]",
            'th': "นี่คือข้อมูลเบื้องต้น: [premise]. อะไรคือ [question]? ช่วยฉันเลือกตัวเลือกที่สมเหตุสมผลมากกว่า: -ตัวเลือก1: [choice1], -ตัวเลือก2: [choice2]",
            'tr': "İşte bir öncül: [premise]. [question] nedir? Daha makul seçeneği seçmeme yardım et: -seçenek1: [choice1], -seçenek2: [choice2]",
            'vi': "Đây là một giả định: [premise]. [question] là gì? Giúp tôi chọn phương án hợp lý hơn: -lựa chọn1: [choice1], -lựa chọn2: [choice2]",
            'zh': "这里有一个前提：[premise]。什么是[question]？请帮我选择更合理的选项：-选项1：[choice1]，-选项2：[choice2]"

        },
        "answer_prompt": {
            'en': 'You should only choose one option for your answer. You should answer the question in format of "Answer: [1 or 2]"',
            'et': 'Sa peaksid oma vastuseks valima ainult ühe variandi. Sa peaksid vastama küsimusele vormis "Vastus: [1 või 2]"',
            'ht': 'Ou ta dwe chwazi sèlman yon opsyon pou repons ou an. Ou ta dwe reponn kesyon an nan fòma "Repons: [1 oswa 2]"',
            'id': 'Anda harus hanya memilih satu opsi untuk jawaban Anda. Anda harus menjawab pertanyaan dalam format "Jawaban: [1 atau 2]"',
            'it': 'Dovresti scegliere solo un\'opzione per la tua risposta. Dovresti rispondere alla domanda nel formato "Risposta: [1 o 2]"',
            'qu': 'Riqsiykipaqa ñaqa akllay hukllaña hukninaypaq. Kaymi riqsiykita kutichiy nisqapi "Kutichiy: [1 utaq 2]"',
            'sw': 'Unapaswa kuchagua chaguo moja tu kwa jibu lako. Unapaswa kujibu swali kwa muundo wa "Jibu: [1 au 2]"',
            'ta': 'நீங்கள் உங்கள் பதிலுக்கு ஒரு விருப்பத்தை மட்டும் தேர்ந்தெடுக்க வேண்டும். நீங்கள் கேள்விக்கு "பதில்: [1 அல்லது 2]" என்ற வடிவில் பதிலளிக்க வேண்டும்',
            'th': 'คุณควรเลือกตัวเลือกเดียวสำหรับคำตอบของคุณ คุณควรตอบคำถามในรูปแบบ "คำตอบ: [1 หรือ 2]"',
            'tr': 'Cevabınız için yalnızca bir seçenek seçmelisiniz. Soruyu "Cevap: [1 veya 2]" formatında yanıtlamalısınız',
            'vi': 'Bạn chỉ nên chọn một phương án cho câu trả lời của mình. Bạn nên trả lời câu hỏi theo định dạng "Câu trả lời: [1 hoặc 2]"',
            'zh': '你应该只选择一个选项作为答案。你应该以“答案：[1 或 2]”的格式回答问题'
        },
        "cot_prompt":{
            "en": "Let's think step-by-step in English.",
            "et": "Mõtleme samm-sammult eesti keeles.",
            "ht": "Ann panse etap pa etap an kreyòl ayisyen.",
            "id": "Mari kita berpikir langkah demi langkah dalam bahasa Indonesia.",
            "it": "Pensiamo passo per passo in italiano.",
            "qu": "Yuyayku paso paso runa simipi.",
            "sw": "Hebu tufikirie hatua kwa hatua kwa Kiswahili.",
            "ta": "நாம் தமிழில் அடுக்கு அடுக்காக சிந்திப்போம்.",
            "th": "ลองคิดทีละขั้นตอนในภาษาไทย.",
            "tr": "Hadi Türkçe adım adım düşünelim.",
            "vi": "Hãy suy nghĩ từng bước bằng tiếng Việt.",
            "zh": "让我们用中文一步一步地思考。"
        },
        "main_prompt":{
            "en": {"cause": "cause", "effect": "effect", "choice1": "Choice1: ", "choice2": "Choice2: "},
            "et": {"cause": "põhjus", "effect": "tagajärg", "choice1": "Valik1: ", "choice2": "Valik2: "},
            "ht": {"cause": "kòz", "effect": "efè", "choice1": "Chwa1: ", "choice2": "Chwa2: "},
            "id": {"cause": "penyebab", "effect": "akibat", "choice1": "Pilihan1: ", "choice2": "Pilihan2: "},
            "it": {"cause": "causa", "effect": "effetto", "choice1": "Scelta1: ", "choice2": "Scelta2: "},
            "qu": {"cause": "paqarin", "effect": "rikchay", "choice1": "Akllay1: ", "choice2": "Akllay2: "},
            "sw": {"cause": "sababu", "effect": "athari", "choice1": "Chaguo1: ", "choice2": "Chaguo2: "},
            "ta": {"cause": "காரணம்", "effect": "விளைவு", "choice1": "விருப்பம்1: ", "choice2": "விருப்பம்2: "},
            "th": {"cause": "สาเหตุ", "effect": "ผลกระทบ", "choice1": "ตัวเลือก1: ", "choice2": "ตัวเลือก2: "},
            "tr": {"cause": "sebep", "effect": "etki", "choice1": "Seçim1: ", "choice2": "Seçim2: "},
            "vi": {"cause": "nguyên nhân", "effect": "tác động", "choice1": "Lựa chọn1: ", "choice2": "Lựa chọn2: "},
            "zh": {"cause": "原因", "effect": "结果", "choice1": "选项1：", "choice2": "选项2："}

        },
    },
    "XNLI": {
        "lang_by_symbol": {
            'en': 'english',
            'fr': 'french',
            'es': 'spanish',
            'de': 'german',
            'el': 'greek',
            'bg': 'bulgarian',
            'ru': 'russian',
            'tr': 'turkish',
            'ar': 'arabic',
            'vi': 'vietnamese',
            'th': 'thai',
            'zh': 'chinese',
            'hi': 'hindi',
            'sw': 'swahili',
            'ur': 'urdu'
        }, 
        "symbol_by_lang": {
            'english': 'en',
            'french': 'fr',
            'spanish': 'es',
            'german': 'de',
            'greek': 'el',
            'bulgarian': 'bg',
            'russian': 'ru',
            'turkish': 'tr',
            'arabic': 'ar',
            'vietnamese': 'vi',
            'thai': 'th',
            'chinese': 'zh',
            'hindi': 'hi',
            'swahili': 'sw',
            'urdu':'ur' 
        },
        "base_prompt": {
            "en": "Given the premise and hypothesis, your task is to judge whether the hypothesis is true, false, or undetermined given the premise. The relationship can be chosen from entailment, contradiction, and neutral.",
            "fr": "Étant donné la prémisse et l'hypothèse, votre tâche est de juger si l'hypothèse est vraie, fausse ou indéterminée compte tenu de la prémisse. La relation peut être choisie parmi l'implication, la contradiction et la neutralité.",
            "es": "Dada la premisa y la hipótesis, tu tarea es juzgar si la hipótesis es verdadera, falsa o indeterminada según la premisa. La relación puede ser elegida entre implicación, contradicción y neutral.",
            "de": "Gegeben sind Prämisse und Hypothese, Ihre Aufgabe ist es zu beurteilen, ob die Hypothese wahr, falsch oder unbestimmt ist, basierend auf der Prämisse. Die Beziehung kann aus Implikation, Widerspruch und Neutralität gewählt werden.",
            "el": "Δεδομένης της προϋπόθεσης και της υπόθεσης, το καθήκον σας είναι να κρίνετε αν η υπόθεση είναι αληθής, ψευδής ή ακαθόριστη βάσει της προϋπόθεσης. Η σχέση μπορεί να επιλεγεί από συνεπαγωγή, αντίφαση και ουδετερότητα.",
            "bg": "Като се дадат предпоставка и хипотеза, вашата задача е да прецените дали хипотезата е вярна, невярна или неопределена спрямо предпоставката. Връзката може да бъде избрана от следствие, противоречие и неутралност.",
            "ru": "Учитывая посылку и гипотезу, ваша задача — определить, является ли гипотеза истинной, ложной или неопределённой в зависимости от посылки. Связь может быть выбрана из следствия, противоречия и нейтральности.",
            "tr": "Önermeyi ve hipotezi dikkate alarak, hipotezin doğru, yanlış veya belirsiz olup olmadığını değerlendirmeniz gerekiyor. İlişki çıkarım, çelişki ve nötr arasından seçilebilir.",
            "ar": "بالنظر إلى المقدمة والافتراض، مهمتك هي الحكم على ما إذا كان الافتراض صحيحًا أو خاطئًا أو غير محدد بناءً على المقدمة. يمكن اختيار العلاقة من التضمين أو التناقض أو الحياد.",
            "vi": "Dựa trên giả thuyết và tiền đề, nhiệm vụ của bạn là đánh giá giả thuyết đó là đúng, sai hay không xác định. Mối quan hệ có thể được chọn từ bao hàm, mâu thuẫn và trung lập.",
            "th": "โดยมีโจทย์และสมมุติฐาน หน้าที่ของคุณคือการตัดสินว่าสมมุติฐานนั้นเป็นจริง เท็จ หรือไม่สามารถระบุได้ตามโจทย์ ความสัมพันธ์สามารถเลือกได้จาก การตามมา ความขัดแย้ง และความเป็นกลาง",
            "zh": "根据前提和假设，你的任务是判断假设在前提下是真的、假的，还是无法确定的。关系可以从蕴含、矛盾和中立中选择。",
            "hi": "दी गई प्रस्तावना और परिकल्पना के आधार पर, आपका कार्य यह निर्णय लेना है कि परिकल्पना सही है, गलत है या अनिर्धारित है। संबंध अनुमान, विरोधाभास और तटस्थता में से चुना जा सकता है।",
            "sw": "Ukipewa dhana na dhana nyingine, kazi yako ni kuhukumu ikiwa dhana hiyo ni kweli, si kweli au haijulikani kulingana na dhana ya awali. Uhusiano unaweza kuchaguliwa kutoka kwa mlingano, mgongano na hali ya kati.",
            "ur": "دی گئی مفروضہ اور قیاس کی بنیاد پر، آپ کا کام یہ فیصلہ کرنا ہے کہ قیاس درست ہے، غلط ہے یا غیر معین ہے۔ تعلق کو استدلال، تضاد اور غیر جانبداری میں سے منتخب کیا جا سکتا ہے۔"
        },
        "answer_prompt": {
            'en': "You should provide the final answer at the end in the format: 'Relationship: [entailment, neutral or contradiction]'.",
            'fr': "Vous devez fournir la réponse finale à la fin au format : 'Relation: [Implication, Neutre ou Contradiction]'.",
            'es': "Debes proporcionar la respuesta final al final en el formato: 'Relación: [Implicación, Neutral o Contradicción]'.",
            'de': "Du solltest die endgültige Antwort am Ende im Format angeben: 'Beziehung: [Implikation, Neutral oder Widerspruch]'.",
            'el': "Πρέπει να δώσεις την τελική απάντηση στο τέλος στη μορφή: 'Σχέση: [Συμπερασματική, Ουδέτερη ή Αντίφαση]'.",
            'bg': "Трябва да предоставите крайния отговор накрая във формат: 'Връзка: [Следствие, Неутрално или Противоречие]'.",
            'ru': "Вы должны дать окончательный ответ в конце в формате: 'Связь: [Следствие, Нейтрально или Противоречие]'.",
            'tr': "Cevabı sonunda şu formatta vermelisin: 'İlişki: [Çıkarım, Nötr veya Çelişki]'.",
            'ar': "يجب أن تقدم الإجابة النهائية في النهاية بالتنسيق: 'العلاقة: [استلزام، حيادي أو تناقض]'.",
            'vi': "Bạn nên cung cấp câu trả lời cuối cùng theo định dạng: 'Mối quan hệ: [Kéo theo, Trung lập hoặc Mâu thuẫn]'.",
            'th': "คุณควรให้คำตอบสุดท้ายในรูปแบบ: 'ความสัมพันธ์: [ตามมา, เป็นกลาง หรือ ขัดแย้ง]'.",
            'zh': "您应该在最后以以下格式提供最终答案：'关系：[蕴含，中立或矛盾]'。",
            'hi': "आपको अंतिम उत्तर इस प्रारूप में देना चाहिए: 'संबंध: निष्कर्ष' या 'संबंध: तटस्थ' या 'संबंध: विरोधाभास'।",
            'sw': "Unapaswa kutoa jibu la mwisho mwishoni kwa muundo: 'Uhusiano: [Ulinganifu, Wastani au Mpingano]'.",
            'ur': "آپ کو آخر میں حتمی جواب اس فارمیٹ میں دینا چاہیے: 'تعلق: [نتیجہ اخذ، غیر جانبدار یا تضاد]'۔"
        },
        "cot_prompt":{
            'en': "Let's think step-by-step in English.",
            'fr': "Réfléchissons étape par étape en français.",
            'es': "Pensemos paso a paso en español.",
            'de': "Lass uns Schritt für Schritt auf Deutsch nachdenken.",
            'el': "Ας σκεφτούμε βήμα προς βήμα στα ελληνικά.",
            'bg': "Нека мислим стъпка по стъпка на български.",
            'ru': "Давайте рассуждать шаг за шагом на русском.",
            'tr': "Haydi adım adım Türkçe düşünelim.",
            'ar': "دعنا نفكر خطوة بخطوة باللغة العربية.",
            'vi': "Hãy suy nghĩ từng bước bằng tiếng Việt.",
            'th': "มาคิดอย่างเป็นขั้นตอนเป็นภาษาไทย.",
            'zh': "让我们用中文一步一步思考.",
            'hi': "आइए हिंदी में चरण दर चरण सोचें.",
            'sw': "Wacha tufikiri hatua kwa hatua kwa Kiswahili.",
            'ur': "آئیے اردو میں مرحلہ وار سوچیں."
        }
    }

}