package target

type Target interface {
	GetName() string
	Check() (bool, error)
}
