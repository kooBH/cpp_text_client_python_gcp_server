#include <string.h>
#include <string>
#include <stdlib.h>
#include <curl.h>
#include <iostream>

#include <vector>

using std::vector;
using std::string;

#define MAX_CHAR_BUF 256

static size_t write_callback(void *ptr, size_t size, size_t nmemb, std::string* data) {
  data->append((char*) ptr, size * nmemb);
  return size * nmemb;
}



int main(){

  string url="127.0.0.1";
  int port=1170;

  CURL* curl_handle;
  CURLcode res;

  string output;

  char post_field[MAX_CHAR_BUF];
  char temp_url[MAX_CHAR_BUF];

  /*** Touch Sequence ***/

  curl_handle = curl_easy_init();


  sprintf(temp_url,"%s:%d",url.c_str(),port);
  /* set URL to get here */ 
  if(curl_handle) {
    curl_easy_setopt(curl_handle, CURLOPT_URL, temp_url);

    curl_easy_setopt(curl_handle, CURLOPT_FOLLOWLOCATION, 1L);

    curl_easy_setopt(curl_handle, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl_handle, CURLOPT_WRITEDATA,     &output);

    res = curl_easy_perform(curl_handle);

    /* Check for errors */ 
    if(res != CURLE_OK)
      fprintf(stderr, "curl_easy_perform() failed: %s\n",
          curl_easy_strerror(res));

    /* always cleanup */ 
    curl_easy_cleanup(curl_handle);
  }

  std::cout<<"Connection Checked."<<std::endl;

  vector<std::string>vec;
  vec.push_back("1.wav");
  vec.push_back("2.wav");
  vec.push_back("3.wav");

  for(auto iter : vec){
    curl_handle = curl_easy_init();

    if(curl_handle) {

      sprintf(temp_url,"%s:%d%s",url.c_str(),port,"/speech");
      curl_easy_setopt(curl_handle, CURLOPT_URL, temp_url);

      sprintf(post_field,"path=%s",iter.c_str());
      curl_easy_setopt(curl_handle, CURLOPT_POSTFIELDS, post_field);

      output="";
      curl_easy_setopt(curl_handle, CURLOPT_WRITEFUNCTION, write_callback);
      curl_easy_setopt(curl_handle, CURLOPT_WRITEDATA,     &output);

      /* Perform the request, res will get the return code */ 
      res = curl_easy_perform(curl_handle);

      /* Check for errors */ 
      if(res != CURLE_OK)
        fprintf(stderr, "curl_easy_perform() failed: %s\n",
            curl_easy_strerror(res));

      /* always cleanup */ 
      curl_easy_cleanup(curl_handle);

      std::cout<<"output : "<<output<<std::endl;
    }

  }

  return 0;
}
