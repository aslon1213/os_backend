package app

import (
	"fmt"
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
	"strings"

	"github.com/aslon1213/os_backend/internal/pkg/handlers"
	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

var NumberOfConnections = 0

type App struct {
	Router   *gin.Engine
	RDMS     *gorm.DB
	Handlers *handlers.Handlers
}

func New() *App {
	app := &App{}
	return app
}

func RedirectTo(c *gin.Context) {

	if strings.Split(c.Request.URL.Path, "/")[1] == "employer" {
		// send request to employer service
		request := c.Request
		client := &http.Client{}
		request.URL.Host = "http://localhost:8000"
		resp, err := client.Do(request)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		defer resp.Body.Close()
		fmt.Fprintf(c.Writer, "Response from employer service: %v", resp)
	}

}

type SimpleProxy struct {
	Proxy *httputil.ReverseProxy
}

func NewProxy(rawUrl string) (*SimpleProxy, error) {
	url, err := url.Parse(rawUrl)
	if err != nil {
		return nil, err
	}
	s := &SimpleProxy{httputil.NewSingleHostReverseProxy(url)}

	// Modify requests
	originalDirector := s.Proxy.Director
	s.Proxy.Director = func(r *http.Request) {
		originalDirector(r)
		// change the path
		// delete /employer/ from the path
		if strings.Contains(r.URL.Path, "/employer/") {
			r.URL.Path = strings.Replace(r.URL.Path, "/employer/", "/", 1)
		} else if strings.Contains(r.URL.Path, "/job_seeker/") {
			r.URL.Path = strings.Replace(r.URL.Path, "/job_seeker/", "/", 1)
		}

	}

	// Modify response
	s.Proxy.ModifyResponse = func(r *http.Response) error {
		// Add a response header
		r.Header.Set("Server", "CodeDodle")

		return nil
	}

	return s, nil
}

func (s *SimpleProxy) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	// Do anything you want here
	// e.g. blacklisting IP, log time, modify headers, etc
	log.Printf("Proxy receives request.")
	log.Printf("Proxy forwards request to origin.")
	NumberOfConnections++
	s.Proxy.ServeHTTP(w, r)
	NumberOfConnections--
	log.Printf("Origin server completes request.")
}

func (app *App) StartApplication() {

	// go func() {
	// 	for {
	// 		fmt.Println("Number of connections: ", NumberOfConnections)
	// 		time.Sleep(1 * time.Second)
	// 	}

	// }()

	employer_proxy, err := NewProxy("http://localhost:8000")
	if err != nil {
		panic(err)
	}
	job_seeker, err := NewProxy("http://localhost:8001")
	if err != nil {
		panic(err)
	}
	http.Handle("/employer/", employer_proxy)
	http.Handle("/job_seeker/", job_seeker)
	log.Fatal(http.ListenAndServe(":8080", nil))
}
