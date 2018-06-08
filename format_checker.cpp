#include <iostream>
#include <string>
#include <vector>
#include <list>
#include <fstream>
#include <sstream>
#include <cstdlib>
#include <math.h>


using namespace std;

class Graph_Node{

private:
	string Node_Name;
	vector<int> Children;
	vector<string> Parents;
	int nvalues;
	vector<string> values;
	vector<float> CPT;

public:
	//Graph_Node(string name, vector<Graph_Node*> Child_Nodes,vector<Graph_Node*> Parent_Nodes,int n, vector<string> vals,vector<float> curr_CPT)
	Graph_Node(string name,int n,vector<string> vals)
	{
		Node_Name=name;
		//Children=Child_Nodes;
		//Parents=Parent_Nodes;
		nvalues=n;
		values=vals;
		//CPT=curr_CPT;

	}
	string get_name()
	{
		return Node_Name;
	}
	vector<int> get_children()
	{
		return Children;
	}
	vector<string> get_Parents()
	{
		return Parents;
	}
	vector<float> get_CPT()
	{
		return CPT;
	}
	int get_nvalues()
	{
		return nvalues;
	}
	vector<string> get_values()
	{
		return values;
	}
	void set_CPT(vector<float> new_CPT)
	{
		CPT.clear();
		CPT=new_CPT;
	}
    void set_Parents(vector<string> Parent_Nodes)
    {
        Parents.clear();
        Parents=Parent_Nodes;
    }
    int add_child(int new_child_index )
    {
        for(int i=0;i<Children.size();i++)
        {
            if(Children[i]==new_child_index)
                return 0;
        }
        Children.push_back(new_child_index);
        return 1;
    }



};



class network{

	list <Graph_Node> Pres_Graph;

public:
	int addNode(Graph_Node node)
	{
		Pres_Graph.push_back(node);
		return 0;
	}
    list<Graph_Node>::iterator getNode(int i)
    {
        int count=0;
        list<Graph_Node>::iterator listIt;
        for(listIt=Pres_Graph.begin();listIt!=Pres_Graph.end();listIt++)
        {
            if(count++==i)
                break;
            
        }
        return listIt;
    }
	int netSize()
	{
		return Pres_Graph.size();
	}
    int get_index(string val_name)
    {
        list<Graph_Node>::iterator listIt;
        int count=0;
        for(listIt=Pres_Graph.begin();listIt!=Pres_Graph.end();listIt++)
        {
            if(listIt->get_name().compare(val_name)==0)
                return count;
            count++;
        }
        return -1;
    }

    list<Graph_Node>::iterator get_nth_node(int n)
    {
       list<Graph_Node>::iterator listIt;
        int count=0;
        for(listIt=Pres_Graph.begin();listIt!=Pres_Graph.end();listIt++)
        {
            if(count==n)
                return listIt;
            count++;
        }
        return listIt; 
    }

    list<Graph_Node>::iterator search_node(string val_name)
    {
        list<Graph_Node>::iterator listIt;
        for(listIt=Pres_Graph.begin();listIt!=Pres_Graph.end();listIt++)
        {
            if(listIt->get_name().compare(val_name)==0)
                return listIt;
        }
    
            cout<<"node not found\n";
        return listIt;
    }
	

};

void check_format()
{
	network Alarm;
	string line,testline;
	int find=0;
  	ifstream myfile("alarm.bif"); 
    ifstream testfile("solved_alarm.bif");
  	string temp;
  	string name;
  	vector<string> values;
  	int line_count=1;
    if (myfile.is_open())
    {

    	while (! myfile.eof() )
    	{
    		
      		getline (myfile,line);
      		
      		
      		

            
            getline (testfile,testline);
            if(testline.compare(line)!=0)
            {
                cout<<"Error Here in line number"<<line_count<<"\n";
                exit(0);
            }
            line_count++;
            stringstream ss;
            ss.str(line);
            ss>>temp;
     		
     		
     		
     		if(temp.compare("probability")==0)
     		{
                    string test_temp;
                    
    				getline (myfile,line);
                    getline (testfile,testline);

     				stringstream ss2;
                    stringstream testss2;
                    ss2.str(line);
     				ss2>> temp;
                    testss2.str(testline);
                    testss2>>test_temp;
                    if(test_temp.compare(temp)!=0)
                    {
                        cout<<"Error Here in line number"<<line_count<<"\n";
                        exit(0);
                    }
     				ss2>> temp;
                    testss2>>test_temp;
     				vector<float> curr_CPT;
                    string::size_type sz;
     				while(temp.compare(";")!=0)
     				{

                        if(!atof(test_temp.c_str()))
                        {
                            cout<<" Probem in Probab values in line "<<line_count<<"\n";
                            exit(0);
     					}
                        //cout<<"here"<<temp<<"\n";
     					ss2>>temp;
                        testss2>>test_temp;
                       
                        

    				}
                    if(test_temp.compare(";")!=0)
                    {
                        cout<<" Probem in Semi-colon in line "<<line_count<<"\n";
                        exit(0);
                    }
                    line_count++;

     		}
            
     		
     		

    		
    		//myfile.close();
    	}
        if(!testfile.eof())
        {
            cout<<" Test File contains more lines\n";
                        exit(0);
        }   
    	//cout<<line;
    	//if(find==1)
    	myfile.close();
        testfile.close();
  	}
  	
  
}

network read_network(char* filename)
{
    network Alarm;
    string line;
    int find=0;
    ifstream myfile(filename); 
    string temp;
    string name;
    vector<string> values;
    
    if (myfile.is_open())
    {
        while (! myfile.eof() )
        {
            stringstream ss;
            getline (myfile,line);
            
            
            ss.str(line);
            ss>>temp;
            
            
            if(temp.compare("variable")==0)
            {
                    
                    ss>>name;
                    getline (myfile,line);
                   
                    stringstream ss2;
                    ss2.str(line);
                    for(int i=0;i<4;i++)
                    {
                        
                        ss2>>temp;
                        
                        
                    }
                    values.clear();
                    while(temp.compare("};")!=0)
                    {
                        values.push_back(temp);
                        
                        ss2>>temp;
                    }
                    Graph_Node new_node(name,values.size(),values);
                    int pos=Alarm.addNode(new_node);

                    
            }
            else if(temp.compare("probability")==0)
            {
                    
                    ss>>temp;
                    ss>>temp;
                    
                    list<Graph_Node>::iterator listIt;
                    list<Graph_Node>::iterator listIt1;
                    listIt=Alarm.search_node(temp);
                    int index=Alarm.get_index(temp);
                    ss>>temp;
                    values.clear();
                    while(temp.compare(")")!=0)
                    {
                        listIt1=Alarm.search_node(temp);
                        listIt1->add_child(index);
                        values.push_back(temp);
                        
                        ss>>temp;

                    }
                    listIt->set_Parents(values);
                    getline (myfile,line);
                    stringstream ss2;
                    
                    ss2.str(line);
                    ss2>> temp;
                    
                    ss2>> temp;
                    
                    vector<float> curr_CPT;
                    string::size_type sz;
                    while(temp.compare(";")!=0)
                    {
                        
                        curr_CPT.push_back(atof(temp.c_str()));
                        
                        ss2>>temp;
                       
                        

                    }
                    
                    listIt->set_CPT(curr_CPT);


            }
            else
            {
                
            }
            
            

            
            
        }
        
        if(find==1)
        myfile.close();
    }
    
    return Alarm;
}

int main()
{
	network Alarm1,Alarm2;
	check_format();
    Alarm1=read_network((char*)"solved_alarm.bif");
    Alarm2=read_network((char*)"gold_alarm.bif");
    float score=0;
    for(int i=0;i<Alarm1.netSize();i++)
    {
        list<Graph_Node>::iterator listIt1=Alarm1.get_nth_node(i);
        list<Graph_Node>::iterator listIt2=Alarm2.get_nth_node(i);
        vector<float> cpt1=listIt1->get_CPT();
        vector<float> cpt2=listIt2->get_CPT();
        for(int j=0;j<cpt1.size();j++)
            score+=fabs(cpt1[j]-cpt2[j]);
    }
   cout <<"Score is "<<score;

	//cout<<Alarm.netSize();
	
}
