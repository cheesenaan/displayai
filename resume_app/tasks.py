
from async_timeout import Timeout
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from .models import Account, Plan, UserProfile
from views import openai_work_experience, openai_project, create_resume
from django.contrib import messages

@shared_task
def reload_resume_and_website(request, account_id):
    try:
        account = Account.objects.get(id=account_id)
        user_plan = Plan.objects.get(account=account)
        user_profile = UserProfile.objects.get(account=account)
        
        work_counter = 1
        for i, work_experience in enumerate(user_profile.work_experiences.all(), start=1):
            if work_counter == 1 or account.tier != "free":
                work_experience.bullet1, work_experience.bullet2, work_experience.bullet3 = openai_work_experience(work_experience.company_name, work_experience.job_title, work_experience.description)
                work_counter = work_counter + 1
            else:
                work_experience.bullet1, work_experience.bullet2, work_experience.bullet3 = "upgrade plan to see optimized bullet" , "upgrade plan to see optimized bullet", "upgrade plan to see optimized bullet"
            work_experience.save()

        for i, project in enumerate(user_profile.projects.all(), start=1):
            if work_counter == 1 or account.tier != "free":
                project.bullet1, project.bullet2 = openai_project(project.project_name, project.description)
                work_counter = work_counter + 1
            else:
                project.bullet1, project.bullet2 = "UPGRADE PLAN FOR OPTIMIZED BULLET" , "UPGRADE PLAN FOR OPTIMIZED BULLET"
            project.save()

        new_resume_link = create_resume(user_profile, account)
        if new_resume_link == "TIME_OUT_ERROR_974":
            messages.error(request, "TIME_OUT_ERROR_974. Could not re-build personal website and resume due to poor internet. Please try again")
            return redirect('confirmation', account_id=account_id)

        user_profile.resume_link = new_resume_link
        account.set_resume_link(new_resume_link)
        print(user_profile.resume_link)

        user_profile.save()
        user_plan.forms_filled_on_current_plan = user_plan.forms_filled_on_current_plan + 1
        user_plan.total_forms_filled = user_plan.total_forms_filled + 1
        account.save()
        user_plan.save()

        messages.success(request, "Using same profile data, resume and personal data has been re-built")

    except Timeout:
        messages.error(request, "Timeout error. Your internet connection is slow. Please try again.")
    except Exception as e:
        messages.error(request, "Unkown error. Please try again.")

    return redirect('confirmation', account_id=account_id)
