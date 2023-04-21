
# favfound (criminalip api)
This code was made to extract the fabicon hash from your desired IP address or URL. You can also see all the IP addresses that are associated with the fabicon hash value. I used an OSINT search engine similar to Shodan and Censys called CriminalIP and the API from their free service.

- In order to receive your criminal-api-key, you have to make an account. (They've recently launched paid plans, but you can also create a free account and access an API key)
- Because of a problem with Python's argparse module, searching for favicons starting with `'-'` (e.g '-82abc4a') is currently unavailable. Please notify me through 'issues' or 'pull request' if a problem occurs



# Installation  

Clone repository:  

```  
$ git clone https://github.com/elihypoo414/favfound.git  
```

```  
$ cd favfound
```

```  
$ python3 -m venv .venv  
$ source .venv/bin/activate  
```

```  
$ pip3 install -r requirements.txt  
```

  

# Usage

```  
$ python3 favfound.py --auth [your-criminalip-api-key]  
```

  

# Optional Arguments  

| Flag                     | MetaVar               | Usage                                                        |
| :----------------------- | :-------------------- | :----------------------------------------------------------- |
| `-A/--auth`              | **API key**           | api authentication with a valid [criminalip.io](http://criminalip.io/) api key |
| `-I/--ip`                | **IP**                | Return favicon hash from an IP                               |
| `-F/--fav-hash-from-ip`  | **Favicon hash**      | Return information about IP which has the favicon hash       |
| `-C/--fav-hash-from-ico` | **Favicon icon path** | Return converted favicon hash from favicon icon              |
| `-W/--fav-hash-from-web` | **Web url**           | Return converted favicon hash from website                   |
| `-O/--output`            | **File Path**         | write output to a file                                       |
| `-R/--read`              | **File Path**         | read file and pretty print the information                   |
