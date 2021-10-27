# Laboratorio 6.2
## Integrantes:
* Julisa Lapa
* José Sanchez

# Preprocesamiento:

El preprocesamiento se da en los siguientes pasos:

## Filtrar los stopwords
Para filtrar los stopwords primero se debe leer el archivo de texto **stoplists.txt** que es el que contiene la lista de las stopwords separados por saltos de línea. Este archivo se lee en la lista **stoplist**. Asimismo, se añade a esta lista algunos símbolos que no se encontraban originalmente y que pueden afectar la tokenización.

Para eliminar los stopwords de una lista de términos se usa la función **clean**. Esta función recibe una lista como parámetro y crea una nueva lista con los mismos elementos donde van a estar los términos finales. Luego, se recorre la lista inicial y, por cada término que esté en stoplist, se elimina esté de la lista de palabras limpias, la cual se retorna al final de la ejecución de la función.

## Reemplazar palabras con su raíz (Stemming)
Para la reducción de palabras se usa el **Snowball Stemmer**, un algoritmo de stemming que permite trabajar con palabras en español. La reducción se aplica en la función **stem** sobre una lista de términos. Esta función crea una lista inicialmente vacía que va a almacenar las palabras reducidas. Luego, se recorre toda la lista que se le pasa como parámetro y a cada término se le aplica la función de reducción del stemmer para luego añadir el término reducido a la lista de palabras reducidas que va a ser retornada al terminar de recorrer la lista.

## Procesar la lista de documentos
El procesamiento de los documentos se hace en la función **readDocuments**. Esta función va a abrir todos los archivos dentro del directorio donde se ubican los documentos, definido al inicio del archivo como **docPath**, va a leer su contenido en la variable **texto**, va a aplicar la tokenización propia de la librería **nltk** para dividir el texto en una lista de términos y, finalmente, va a aplicar sobre esta lista las funciones para el filtrado de stopwords y la reducción. La lista resultante se va a guardar en un diccionario que va a mapear el ID de cada documento con la lista de términos en este. El diccionario se retorna al terminar de analizar todos los documentos.

# Construcción del índice invertido:

La implementación del índice invertido se hizo en una clase denominada **InvertedIndex** que va a contener los métodos para su contrucción así como los métodos para hacer las consultas booleanas.

## Estructura de la clase
La clase del **InvertedIndex** tiene dos atributos **filename**, que guarda el nombre del archivo de texto en el que se va a almacenar el índice, y **index**, diccionario que guarda el índice en sí y que mapea cada término con una lista compuesta por la frecuencia del término y la lista de los IDs de los documentos en los que aparece.

El constructor de la clase recibe y asigna el valor de **filename** y llama a la función **createIndex** la cual construye el **index**. La función **write** escribe el **index** en el archivo de texto con el nombre de **filename**. La función **L** recibe un término y retorna la lista de publicaciones asociadas a este. Finalmente, las funciones **AND**, **OR** y **AND_NOT** aplican las operaciones respectivas sobre dos términos.

## Construcción de index
La función **createIndex** primero llama a la función **readDocuments** y almacena el valor retornado en el diccionario **docs**. Luego, recorre la lista de términos de cada documento para almacenar en la lista **tokens** todos los términos en el conjunto de documentos. Se almacenan estos términos sin repeticiones usando un set en otra lista **tokensSet** que se recorre para guardar los pares de términos y su frecuencia en todos los documentos, calculada en base a la lista original de términos, en la lista **tokenFreq**. Esta lista se ordena de modo que al final se ubiquen al final los términos que tienen una mayor frecuencia y, de haber empates, se ordenen en orden alfabético. De este modo, podemos extraer los últimos 500 elementos de la lista para tener los 500 términos más frecuentes de toda la colección priorizandolos según orden alfabético en el caso de que tengan la misma frecuencia. Finalmente, esta lista es ordenada y recorrida para agregar sus contenidos al índice. Antes de finalizar la función, se llama a **write** para escribir el índice recién creado en un archivo de texto.

## Escritura en archivo de texto
Para la escritura primero se abre el archivo con el nombre definido en **filename** y se crea de no existir. Luego, se hace un recorrido por **index** escribiendo cada término con la lista de documentos asociado a este según el formato solicitado. Al finalizar, se cierra el archivo.

# Consultas booleanas:

Las consultas booleanas implementadas en el índice son las de **AND**, **OR** y **AND_NOT**. Asimismo, se implementó la función **L** que recibe un término y retorna la lista de documentos asociados a este. Esta función también puede recibir como parámetro una lista, cosa que se puede dar al hacer consultas consecutivas, en cuyo caso retorna la misma lista.

## AND
La función **AND** recibe dos términos. Primero, se recuperan las listas de los documentos asociados a cada término llamando a la función **L** para cada uno y se agrega al final de cada una -1, valor que va a servir para identificar que se llegó al final de la lista. También se declaran las variables **p1** y **p2**, inicialmente en 0, que van a servir como índices para las listas. Luego de esto, se entra al bucle while donde se implementa el algoritmo de mezcla. Mientras ambas listas no hayan sido leídas por completo, es decir los valores en las posiciones de sus índices p1 y p2 no es -1, se va a ejecutar el bucle. Si los valores de las listas en sus respectivas posiciones son iguales, entonces se añade el valor a la lista resultante pues se cumple la condición AND y se avanzan ambos índices para acceder a los elementos siguientes en ambas listas. De no ser así, avanza el puntero de la lista cuyo elemento sea menor pues ambas listas están ordenadas. Al finalizar, se retorna la lista resultante. 

## OR
La función **OR** funciona de manera similar a **AND** con la diferencia de que no solo se añaden elementos a la lista resultante si los valores en las posiciones respectivas de ambas listas son iguales, sino que también cuando no lo son, esto para cumplir con la condición del operador OR. Asimismo, puede ocurrir que cuando se salga del bucle una lista no haya sido leída por completo, para lo cual se añaden dos bucles while, uno por cada lista, luego del principal que van a añadir a la lista resultante los elementos restantes en caso no se hayan terminado de leer de modo que al finalizar la función se tengan todos los IDs de los documentos en los que aparece al menos uno de los términos.

## AND_NOT
La función **AND_NOT** funciona de manera similar a **AND** con la diferencia de que solo se añaden elementos a la lista resultante cuando el índice de la lista del primer término avanza, es decir cuando el elemento de la primera lista sea menor al de la segunda, y ya no cuando sean iguales. Esto va a hacer que en la lista resultantes estén solo los documentos que contienen al primer término más no al segundo.

## Prueba del programa
Para probar la funcionalidad del programa se ejecutaron las consultas (Gandalf AND Frodo) AND NOT Gondor, Orthanc OR (Anillo AND NOT Nazgûl) y (Merry AND Hobbit) OR Gimli. Los resultados obtenidos fueron los siguientes:

