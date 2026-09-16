1. Problem Statement and Target Users

Problem. During shift handovers, important information can sometimes be missed or misunderstood. The staff ending their shift may explain what they completed and what still needs to be done, but this is often done through a quick verbal update or short notes. When the next shift starts, they may not have a clear idea of what has already been done or what they need to follow up on.

This can lead to tasks being missed, repeated, or forgotten. If a task is carried forward from one shift to another without being properly followed up, it may continue to be overlooked until it becomes a bigger problem.

This project aims to provide a simple way for shift leaders to record their handover information and help make sure important unfinished tasks are not forgotten.

Target users. The main users are shift leaders. The outgoing shift leader will use the system to record what happened during their shift, while the incoming shift leader can use the information to understand what has been completed and what still needs their attention.

2. User Inputs

The shift leader will provide the following information:
Tasks that were completed during the shift
Tasks that still need to be done by the next shift
Any important remarks, such as safety concerns, equipment problems, or unusual situations

3. Use of AI

The system will use AI to help understand the notes written by the shift leader. It will look at the current shift's notes together with the previous shift's handover information.

The purpose is to work out which tasks have actually been completed and which tasks are still unfinished. For example, one person might write "completed the evening safety walk-through", while the previous shift wrote "safety walk-through still needs to be done". Even though the wording is different, the AI can understand that they are talking about the same task.

The AI will provide the following information:

Completed items – tasks that were finished during the current shift
Pending items – tasks that still need to be done
Carried-over items – tasks from the previous shift that are still unfinished

The AI is mainly used to help understand the meaning of the notes.

4. Business Rules

The system will follow several rules to make sure unfinished tasks are properly followed up:

Unfinished tasks are carried forward – Tasks not completed during the shift will be passed to the next shift.
Repeated unfinished tasks are highlighted – Tasks unfinished for 3 or more shifts will be marked "Overdue – Needs Supervisor Attention."
Urgent issues are shown first – Urgent or safety-related issues will appear at the top.
Unclear information needs to be checked – Low-confidence results will require the shift leader to review and confirm them.
At least one task is required – The leader must enter at least one completed or pending task.
Keep notes short – Long task descriptions will be flagged and shortened.
Clear presentation – Handover information will be grouped into Completed, Pending, Carried Over, and Remarks.
