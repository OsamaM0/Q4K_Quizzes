from langdetect import detect
import asyncio
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from bot.modules.translator import translate
from g4f import models
from .g4f_llm import G4FLLM

class AIModules:
    def __init__(self, model=None):
        # Set up the LLM (default is GPT-3.5-turbo)
        self.llm = G4FLLM(
            model=model if model else models.gpt_4o
        )

    def detect_language(self, text):
        """Detects the language of the input text."""
        return detect(text)

    def get_prompt_template(self, text, english_template, arabic_template):
        """Returns the appropriate template based on the detected language."""
        language = self.detect_language(text)
        if language == 'ar':
            return arabic_template
        else:
            return english_template

    # Modify the quiz generation function to use language-specific templates
    async def generate_quiz(self, text):
        """Generates a quiz from the input text asynchronously."""
        english_template = PromptTemplate(
            input_variables=["text"],
            template="""
            Pretend you are a teacher preparing a quiz for the text I will provide. 
            Each quiz question should follow the format below. 
            Ensure that you carefully recheck the questions and answers for accuracy. 
            The output should be a ready-to-use list of dictionaries for the Python eval function:

            [

                    "question": "WRITE THE QUESTION HERE",
                    "options": ["A) OPTION_1", "B) OPTION_2", "C) OPTION_3", "D) OPTION_4"],
                    "answer": INDEX_OF_CORRECT_ANSWER_IN_OPTIONS_LIST,
                    "explanation": "EXPLAIN WHY THE ANSWER IS CORRECT"

            ]

            Text:
            {text}

            Quiz:
            """
        )

        arabic_template = PromptTemplate(
            input_variables=["text"],
            template="""
            قم بإعداد اختبار للنص الذي سأقدمه لك. 
            يجب أن يتبع كل سؤال في الاختبار التنسيق التالي. 
            تأكد من إعادة فحص الأسئلة والإجابات بدقة للتأكد من صحتها.
            يجب أن تكون النتيجة قائمة جاهزة للاستخدام من القواميس للوظيفة eval في بايثون:

            [

                    "السؤال": "اكتب السؤال هنا",
                    "الخيارات": ["أ) الخيار 1", "ب) الخيار 2", "ج) الخيار 3", "د) الخيار 4"],
                    "الإجابة": الفهرس_الصحيح_للإجابة_من_قائمة_الخيارات,
                    "التفسير": "اشرح سبب صحة الإجابة"

            ]

            النص:
            {text}

            الاختبار:
            """
        )

        # Choose the correct template based on language
        quiz_template = self.get_prompt_template(text, english_template, arabic_template)
        chain = LLMChain(llm=self.llm, prompt=quiz_template)
        questions = await asyncio.to_thread(chain.invoke, text)
        questions = questions["text"]
        if self.detect_language(text) != self.detect_language(questions):
            return await translate(questions, self.detect_language(text))

        return questions



    # 2. Summarize Text
    async def summarize_text(self, text):
        """Summarizes the provided text asynchronously."""
        english_template = PromptTemplate(
            input_variables=["text"],
            template="Summarize the following text to main points and sub-points and make detailed explain for them:\n\n{text}\n\nSummary :"
        )
        arabic_template = PromptTemplate(
            input_variables=["text"],
            template="قم بتلخيص هذا النص ال النقط الرئيسية ونقط فرعيه وشرح مفصل لهذة النقط الرئيسية والنقط فرعيه:\n\n{text}\n\nالملخص :"
        )

        # Choose the correct template based on language
        summary_template = self.get_prompt_template(text, english_template, arabic_template)
        chain = LLMChain(llm=self.llm, prompt=summary_template)
        summary = await asyncio.to_thread(chain.invoke, text)
        summary = summary["text"]
        if self.detect_language(text) != self.detect_language(summary):
            return await translate(summary, self.detect_language(text))

        return summary


    async def split_text_with_overlap(self, text, chunk_size=9000, overlap_size=2000):
        """Splits text into overlapping chunks to maintain context."""
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunks.append(text[start:end])
            start += chunk_size - overlap_size  # Move by chunk size minus the overlap
        return chunks

    async def generate_summary(self, text, chunk_size=9000, overlap_size=2000):
        """Summarizes large text with hierarchical summarization and sliding window overlap."""
        # Split text into overlapping chunks
        text_chunks = await self.split_text_with_overlap(text, chunk_size, overlap_size)

        # Summarize each chunk individually
        chunk_summaries = []
        for chunk in text_chunks:
            summary = await self.summarize_text(chunk)
            chunk_summaries.append(summary["text"])

        # Combine the individual chunk summaries
        combined_summaries = " ".join(chunk_summaries)

        # Summarize the combined summaries to get a final concise output
        final_summary = await self.summarize_text(combined_summaries)

        return final_summary
        

    # 3. Generate Q&A
    async def generate_qa(self, text):
        """Generates questions and answers based on the input text."""
        qa_template = PromptTemplate(
            input_variables=["text"],
            template="""
            Create questions and answers based on the following text. Provide a ready-to-use list of dictionaries for the Python eval function:

            [

                    "question": "WRITE THE QUESTION HERE",
                    "answer": "CORRECT ANSWER"

            ]

            Text:
            {text}

            Questions and Answers:
            """
        )
        chain = LLMChain(llm=self.llm, prompt=qa_template)
        return await asyncio.to_thread(chain.invoke, text)

    # 4. Explain a Concept
    async def explain_concept(self, concept):
        """Explains a concept in simple terms asynchronously."""
        explain_template = PromptTemplate(
            input_variables=["concept"],
            template="""
            Explain the following concept in simple terms for a student to understand:

            Concept: {concept}

            Explanation:
            """
        )
        chain = LLMChain(llm=self.llm, prompt=explain_template)
        return await asyncio.to_thread(chain.invoke, concept)

    # 5. Generate Flashcards
    async def generate_flashcards(self, text):
        """Generates flashcards from the text for studying."""
        flashcard_template = PromptTemplate(
            input_variables=["text"],
            template="""
            Create flashcards from the following text. Each flashcard should have a question on the front and an answer on the back. Provide the output as a list of dictionaries for the Python eval function:

            [

                    "question": "FLASHCARD QUESTION",
                    "answer": "FLASHCARD ANSWER"

            ]

            Text:
            {text}

            Flashcards:
            """
        )
        chain = LLMChain(llm=self.llm, prompt=flashcard_template)
        return await asyncio.to_thread(chain.invoke, text)

    # 6. Generate Practice Problems
    async def generate_practice_problems(self, subject, topic):
        """Generates practice problems for a specific subject and topic."""
        problem_template = PromptTemplate(
            input_variables=["subject", "topic"],
            template="""
            Generate five practice problems for the following subject and topic. 
            Ensure that the problems vary in difficulty and provide solutions for each problem:

            Subject: {subject}
            Topic: {topic}

            Problems:
            """
        )
        chain = LLMChain(llm=self.llm, prompt=problem_template)
        return await asyncio.to_thread(chain.invoke, subject=subject, topic=topic)

    # 7. Generate Essay Questions
    async def generate_essay_questions(self, subject, topic):
        """Generates essay-style questions for critical thinking."""
        essay_template = PromptTemplate(
            input_variables=["subject", "topic"],
            template="""
            Create three essay-style questions that encourage critical thinking for the following subject and topic:

            Subject: {subject}
            Topic: {topic}

            Essay Questions:
            """
        )
        chain = LLMChain(llm=self.llm, prompt=essay_template)
        return await asyncio.to_thread(chain.invoke, subject=subject, topic=topic)

    # 8. Detailed Topic Breakdown
    async def breakdown_topic(self, topic):
        """Breaks down a complex topic into smaller subtopics for better understanding."""
        breakdown_template = PromptTemplate(
            input_variables=["topic"],
            template="""
            Break down the following topic into smaller, digestible subtopics. 
            Provide explanations for each subtopic for better understanding:

            Topic: {topic}

            Breakdown:
            """
        )
        chain = LLMChain(llm=self.llm, prompt=breakdown_template)
        return await asyncio.to_thread(chain.invoke, topic)





# # Example usage with async
# async def main():
#     processor = TextProcessor()

#     text = data
#     subject = "Mathematics"
#     topic = "Calculus"

#     # Generate quiz asynchronously
#     quiz = await processor.generate_quiz(text)
#     print("Quiz Generated:", quiz)

#     # Summarize text asynchronously
#     summary = await processor.summarize_text(text)
#     print("Summary:", summary)

#     # Generate Q&A asynchronously
#     qa = await processor.generate_qa(text)
#     print("Q&A Generated:", qa)

#     # Explain a concept asynchronously
#     explanation = await processor.explain_concept("Photosynthesis")
#     print("Explanation:", explanation)

#     # Generate flashcards asynchronously
#     flashcards = await processor.generate_flashcards(text)
#     print("Flashcards Generated:", flashcards)

#     # Generate practice problems asynchronously
#     problems = await processor.generate_practice_problems(subject, topic)
#     print("Practice Problems Generated:", problems)

#     # Generate essay questions asynchronously
#     essay_questions = await processor.generate_essay_questions(subject, topic)
#     print("Essay Questions Generated:", essay_questions)

#     # Break down topic asynchronously
#     breakdown = await processor.breakdown_topic(topic)
#     print("Topic Breakdown:", breakdown)

# # invoke the async main function
# if __name__ == "__main__":
#     asyncio.invoke(main())
