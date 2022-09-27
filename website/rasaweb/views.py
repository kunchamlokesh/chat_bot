from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rasaweb.utils import haystack_qa
import logging
from rasaweb.utils import service_now
from rasaweb.utils import learning_recommendation,duckduckgo_search_util

logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.INFO)


# Create your views here.
from django.contrib.auth import authenticate, login,logout
def index(request):
    # if request.user.is_authenticated:
    return render(request,'index.html')



class Get_Answer(APIView):
    """
    Get the answer for question.
    """
    # Returns a json serialized version of the batches when called.
    # Used in the browseable API.
    def get(self, request,question, format=None):
        question = str(question)
        logging.info('in api "get" batch list function')
        res = haystack_qa.get_answer(question)
        if res=="Search":
            res = duckduckgo_search_util.search_duckduckgo(question)
        return Response(res)

    # #This method is called when you post a BatchOfTests
    # def post(self, request, format=None):
    #     logging.info('in api "post" batch list function')
    #     serializer = BatchSerializer(data=request.DATA)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Create_Ticket(APIView):
    def post(self, request, format=None):
        logging.info('in api "post" batch list function')
        data=request.data
        short_description = ""
        description = ""
        for key,value in data.items():
            print(key)
            if key=="short_description":
                short_description=short_description+value
            elif key=="description":
                description = description+value
        res = service_now.create_ticket(short_description,description)
        print(res)
        return Response(res)

    def get(self,request,inc):
        response_dict = {}
        res = service_now.get_ticket_details(inc)
        if "error" in res.keys():
            status = "No Record Found"
            response_dict[inc] = status
        else:
            status_id = res['result'][0]['incident_state']
            status_dict = {2: "In Progress", 3: "On Hold" ,6:"Resolved", 7: "Closed",1:"New"}
            status = status_dict.get(status_id,"Pending")
        response_dict[inc] = status

        return Response(response_dict)





class Machine_Recommendation(APIView):
    def get(self,request,format=None):
        courses = learning_recommendation.search_based_on_intreset_domain(request.user.account.Domain,request.user.account.Area_of_Interest)
        res_dict = {}
        filtered_values = [ "course_id","course_title","url","level"]
        for course, details in courses.items():
            if course in filtered_values:
                id_list = courses[course].keys()
                for i in id_list:
                    course_details_list = []
                    course_id = courses[filtered_values[0]][i]
                    course_title = courses[filtered_values[1]][i]
                    course_url = courses[filtered_values[2]][i]
                    course_level = courses[filtered_values[3]][i]
                    course_details_list.append(course_title)
                    course_details_list.append(course_url)
                    course_details_list.append(course_level)
                    res_dict[course_id] = course_details_list

        return Response(res_dict)


