package main

import "github.com/gin-gonic/gin"

type LinkURL struct {
	Shortlink string `uri:"shortlink" binding:"required"`
}

func index(c *gin.Context) {
	c.JSON(200, gin.H{
		"message": "pastelink go backend",
	})
}

func redirect(c *gin.Context) {
	var link LinkURL
	if err := c.ShouldBindUri(&link); err != nil {
		c.JSON(400, gin.H{"msg": err})
		return
	} else {
		c.JSON(200, gin.H{
			"item": link,
			"dude": "awesome",
		})
		return
	}
}

func main() {
	r := gin.Default()
	r.GET("/", index)
	r.GET("/l/:shortlink", redirect)
	r.Run(":7000")
}
