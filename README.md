# sign_language_datasets
A single library to (down)load all existing sign language video datasets.

There are [various video datasets](http://facundoq.github.io/unlp/sign_language_datasets/) for Sign Language. However:
* Each dataset has its own format and many are hard to find. 
* Each dataset has its own mapping of handshapes to classes. While Signs depend on the specific Sign Language for a country/region, handshapes are universal. Hence, they could be shared between datasets/tasks. 

This library aims to provide two main features:
* A simplified API to download and load datasets
* A mapping between datasets so that datasets can be merged for training/testing models.

We hope it will help Sign Language Recognition develop further, both for research and application development.

If you wish to add a dataset you can make a push request or file an issue.  
    
This library is a *work in progress*. Contributions are welcome.





