L'applicazione sviluppata è un social network con funzionalità simili a Twitter. Ciascun utente può creare un proprio profilo che comprende un nome, un'immagine profilo e una biografia. Una volta registrato un utente può pubblicare un tweet che comprende: un testo, la data di pubblicazione, un'eventuale immagine, una categoria e un numero di like ricevuti. Gli utenti si suddividono in due tipologie: gli utenti anonimi e quelli registrati. I primi possono interagire con l'applicazione vedendo una lista degli ultimi 20 tweet pubblicati da un qualsiasi utente per ordine di data, ricercare un utente tramite il nome, ricercare un tweet tramite categoria o testo e infine registrarsi. Gli utenti registrati oltre a tutte le funzionalità di quelli anonimi possono anche: creare, modificare ed eliminare un tweet, seguire dei profili, lasciare like ad un tweet, visualizzare i tweet solo dagli utenti seguiti.
Ogni profilo è pubblico, chiunque, anche se non registrato, può visualizzare i tweet pubblicati.
### Modelli utilizzati
L'applicazione utilizza 4 Modelli: 
1. User: modello fornito da django
2. Profile: che rappresenta il profilo di un singolo utente, quindi comprenderà un nome (che in fase di registrazione viene impostato uguale allo username del modello User), una foto profilo che viene impostata di default, una biografia opzionale
3. Tweet: che rappresenta un singolo tweet, quindi comprende un autore che è foreign key del modello profilo, un testo obbligatorio, un'immagine opzionale, una categoria da scegliere tra le 12 presenti nell'applicazione, una data di pubblicazione che viene impostata di default e un campo LikedBy che sarà una lista di profili che hanno messo like al tweet.
4. UserFollowing: che rappresenta una relazione di following, ovvero il profilo della colonna Profile segue il profilo della colonna Following

### Organizzazione dell'applicazione
L'applicazione è stata suddivisa in un'unica app chiamata `main` che contiene tutte le views utilizzare, ad eccezione di quelle per la gestione di registrazione/login/logout che vengono gestite da django e sono presenti nella cartella `twitter_clone`.

##### Urls
Gli url pattern associati alle views dell'app `main` sono:
+ `home/` per la visualizzazione degli ultimi 20 tweet in ordine di data di pubblicazione
+ `feed/` riservata agli utenti loggati, per la visualizzazione dei tweet dagli account che seguiamo
+ `tweet/<pk>` per visualizzare un singolo tweet
+ `profile/<pk>` per visualizzare nel dettaglio un singolo profilo 
+ `myprofile/`: riservata agli utenti loggati per visualizzare il proprio profilo
+ `createtweet/` riservata agli utenti loggati, per la creazione di un tweet
+ `updatetweet/<pk>`riservata agli utenti loggati, per modificare un tweet, controlla che l'utente sia l'effettivo autore del tweet
+ `deletetweet/<pk>`riservata agli utenti loggati, per eliminare un tweet, controlla che l'utente sia l'effettivo autore del tweet
+ `/updateprofile/<pk>`riservata agli utenti loggati, permette di aggiornare i dati del proprio profilo, controlla che l'utente sia l'effettivo proprietario del profilo
+ `liketweet/`riservata agli utenti loggati, viene chiamata ogni volta che un utente vuole mettere oppure togliere un like. 
+ `follow/` riservata agli utenti loggati, viene chiamata quando un utente vuole iniziare o smettere di seguire un altro
+ `searchprofile/` permette di cercare un profilo tramite nome
+ `searchprofileresults/<str:name>` Restituisce i profili (se esistono) che l'utente vuole cercare dalla `searchprofile/` 
+ `searchtweet/`: permette di cercare un tweet tramite stringa (opzionale) e categoria
+ `searchtweetresults/<str:category>/<str:text>`: Restituisce i tweet (se esistono) che l'utente vuole cercare da `searchtweet/`

### Test
Sono stati effettuati i test su due Class Based View:
1. TweetListView: la view associata alla home page dove vengono mostrati gli ultimi 20 tweet pubblicati da qualsiasi utente. In particolare vengono controllati 2 casi:
	1. Nessun tweet pubblicato: viene controllato che nel template sia presente la stringa: `Non ci sono tweet da mostrare`
	2. Un tweet pubblicato: viene creato il tweet e viene controllato che esso sia presente nel context della responce della view
2. FeedView: la view che mostra tutti i tweet dagli account seguiti, in particolare sono stati testati 2 casi:
	1. nessun account seguito: viene creato un profilo che non ne segue e si controlla che nella pagina feed non ci siano tweet presenti, ovvero  che nel template sia presente la stringa: `Non ci sono tweet da mostrare`
	2. un account seguito con un tweet pubblicato: viene creato un profilo e pubblicato un tweet, successivamente viene creato un secondo profilo che segue il primo e viene controllato che nella pagina feed sia presente il tweet creato


